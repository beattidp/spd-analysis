import numpy as np

def fibonacci_lattice(n):
    """
    Generate n points on a sphere using the Fibonacci Lattice algorithm.
    """
    i = np.arange(0, n, dtype=float)
    phi = np.pi * (3.0 - np.sqrt(5.0))  # golden angle
    
    z = 1 - (i / float(n - 1)) * 2  # z goes from 1 to -1
    radius = np.sqrt(1 - z * z)  # radius at z
    
    theta = phi * i  # golden angle increment
    
    x = np.cos(theta) * radius
    y = np.sin(theta) * radius
    
    return np.column_stack((x, y, z))

def saff_kuijlaars(n):
    """
    Generate n points on a sphere using the Saff-Kuijlaars Spiral method.
    """
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
    
    return np.column_stack((x, y, z))

def kogan_2017(n):
    """
    Generate n points on a sphere using the Kogan (2017) method.
    """
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
    
    return np.column_stack((x, y, z))
