import numpy as np
from scipy.spatial import cKDTree

def spherical_distance(euclidean_dist):
    """
    Converts 3D Euclidean distance to spherical distance (great-circle distance)
    on a unit sphere.
    """
    # Ensure domain is valid due to float inaccuracies
    euclidean_dist = np.clip(euclidean_dist, 0.0, 2.0)
    return 2.0 * np.arcsin(euclidean_dist / 2.0)

def analyze_points(points):
    """
    Given an (N, 3) array of points on a unit sphere,
    compute min_dist, max_dist, and std_dev of the nearest neighbor spherical distances.
    """
    if len(points) < 2:
        return 0.0, 0.0, 0.0
        
    tree = cKDTree(points)
    
    # Query 2 nearest neighbors: self and the actual nearest neighbor
    distances, indices = tree.query(points, k=2)
    
    # Extract the distance to the actual nearest neighbor (which is the 2nd column)
    nearest_euclidean = distances[:, 1]
    
    # Convert to spherical distance
    nearest_spherical = spherical_distance(nearest_euclidean)
    
    min_dist = np.min(nearest_spherical)
    max_dist = np.max(nearest_spherical)
    std_dev = np.std(nearest_spherical)
    
    return min_dist, max_dist, std_dev

def latitudinal_analysis(points, num_bins=18):
    """
    Analyze the standard deviation of nearest neighbor distances grouped by latitudinal bands.
    
    num_bins=18 means 10-degree bins for 180 degrees (-pi/2 to pi/2).
    """
    if len(points) < 2:
        return []
        
    # Z coordinate maps to latitude (if pole is Z-axis)
    z = points[:, 2]
    # Latitude ranges from -pi/2 to pi/2. Convert z to latitude:
    latitude = np.arcsin(np.clip(z, -1.0, 1.0))
    
    tree = cKDTree(points)
    distances, _ = tree.query(points, k=2)
    nearest_spherical = spherical_distance(distances[:, 1])
    
    # Define bin edges from -pi/2 to pi/2
    bins = np.linspace(-np.pi/2, np.pi/2, num_bins + 1)
    
    # Digitize latitudes into bins (returns bin indices 1 to num_bins)
    # Adding a small epsilon to the last bin to include pi/2
    bins[-1] += 1e-8 
    bin_indices = np.digitize(latitude, bins)
    
    results = []
    
    for b in range(1, num_bins + 1):
        mask = (bin_indices == b)
        pts_in_bin = nearest_spherical[mask]
        
        # Midpoint of the bin in degrees for clear plotting/understanding
        lat_deg = np.degrees((bins[b-1] + bins[b]) / 2.0)
        
        if len(pts_in_bin) > 0:
            std_dev = float(np.std(pts_in_bin))
            mean_dist = float(np.mean(pts_in_bin))
        else:
            std_dev = np.nan
            mean_dist = np.nan
            
        results.append({
            "latitude_deg": lat_deg,
            "std_dev": std_dev,
            "mean_dist": mean_dist,
            "count": len(pts_in_bin)
        })
        
    return results
