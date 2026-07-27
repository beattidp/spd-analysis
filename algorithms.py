import numpy as np

class SphericalDistribution:
    """Base class for spherical point distribution algorithms."""
    def generate(self, n):
        raise NotImplementedError("Subclasses must implement generate()")

class FibonacciLattice(SphericalDistribution):
    def generate(self, n):
        i = np.arange(0, n, dtype=float)
        phi = np.pi * (3.0 - np.sqrt(5.0))  # golden angle
        
        z = 1 - (i / float(n - 1)) * 2  # z goes from 1 to -1
        radius = np.sqrt(1 - z * z)  # radius at z
        
        theta = phi * i  # golden angle increment
        
        x = np.cos(theta) * radius
        y = np.sin(theta) * radius
        
        return np.column_stack((x, y, z))

class SaffKuijlaars(SphericalDistribution):
    def generate(self, n):
        k = np.arange(1, n+1, dtype=float)
        h = -1.0 + 2.0 * (k - 1) / (n - 1)
        h[0] = -1.0
        h[-1] = 1.0
        
        theta = np.arccos(h)
        phi = np.zeros(n)
        
        for i in range(1, n-1):
            phi[i] = (phi[i-1] + 3.6 / np.sqrt(n) * 1.0 / np.sqrt(1.0 - h[i]**2)) % (2*np.pi)
            
        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)
        
        # Reverse the points so z goes from 1 to -1 (to match Fibonacci orientation for easy hybridizing)
        pts = np.column_stack((x, y, z))
        return pts[::-1]

class Kogan2017(SphericalDistribution):
    def generate(self, n):
        x_val = 0.1 + 1.2 * n
        start = -1.0 + 1.0 / (n - 1.0)
        increment = (2.0 - 2.0 / (n - 1.0)) / (n - 1.0)
        
        j = np.arange(0, n, dtype=float)
        s = start + j * increment
        
        ang1 = s * x_val
        ang2 = (np.pi / 2.0) * np.sign(s) * (1.0 - np.sqrt(1.0 - np.abs(s)))
        
        x = np.cos(ang1) * np.cos(ang2)
        y = np.sin(ang1) * np.cos(ang2)
        z = np.sin(ang2)
        
        pts = np.column_stack((x, y, z))
        # Reverse to align z from 1 to -1
        return pts[::-1]

class HybridDistribution(SphericalDistribution):
    """
    Combines two algorithms by applying a polar algorithm above a certain absolute latitude
    and an equatorial algorithm below it.
    """
    def __init__(self, polar_algo, equatorial_algo, transition_lat_deg=60.0):
        self.polar_algo = polar_algo
        self.equatorial_algo = equatorial_algo
        self.transition_z = np.sin(np.radians(transition_lat_deg))
        
    def generate(self, n):
        pts_polar = self.polar_algo.generate(n)
        pts_equator = self.equatorial_algo.generate(n)
        
        # Both algorithms should output z in descending order (1 to -1) based on the refactor.
        # We can just conditionally select points based on their Z coordinate.
        z = pts_polar[:, 2] # Use the Z coordinate
        
        # Mask for polar region
        is_polar = np.abs(z) >= self.transition_z
        
        # Combine
        combined_pts = np.where(is_polar[:, np.newaxis], pts_polar, pts_equator)
        return combined_pts

# Backward compatible function wrappers
def fibonacci_lattice(n):
    return FibonacciLattice().generate(n)

def saff_kuijlaars(n):
    return SaffKuijlaars().generate(n)

def kogan_2017(n):
    return Kogan2017().generate(n)
