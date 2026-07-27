import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

nb.cells = [
    nbf.v4.new_markdown_cell("# Hybrid Polar-Equatorial Distribution Study\nThis study demonstrates how to mathematically combine two point distribution algorithms by switching between them at specific latitudinal boundaries (e.g., merging Saff-Kuijlaars for polar regions and Fibonacci Lattice for equatorial regions)."),
    
    nbf.v4.new_code_cell("""import sys
import os

# Append project root to sys.path so we can import from the main project
project_root = os.path.abspath(os.path.join(os.getcwd(), '../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from IPython.display import HTML

# Import the newly refactored class hierarchy
from algorithms import FibonacciLattice, SaffKuijlaars, HybridDistribution
from metrics import analyze_points, latitudinal_analysis
"""),

    nbf.v4.new_markdown_cell("## Constructing the Hybrid Model\nWe initialize the base algorithms and combine them into a `HybridDistribution` that transitions at exactly 60 degrees latitude (both North and South poles)."),

    nbf.v4.new_code_cell("""# Instantiate base classes
polar_model = SaffKuijlaars()
equatorial_model = FibonacciLattice()

# Create a Hybrid model that transitions at 60 degrees latitude
hybrid_model = HybridDistribution(polar_algo=polar_model, 
                                  equatorial_algo=equatorial_model, 
                                  transition_lat_deg=60.0)

# We wrap the generate method for our metric tools which expect a function
def hybrid_algo(n):
    return hybrid_model.generate(n)

def saff_algo(n):
    return polar_model.generate(n)

def fibo_algo(n):
    return equatorial_model.generate(n)
"""),

    nbf.v4.new_markdown_cell("## 3D Visualization\nVisually comparing the pure algorithms against the new hybrid combination. The points are colored red for polar regions and blue for the equatorial region to visualize the exact slicing threshold."),
    
    nbf.v4.new_code_cell("""n_points = 1000

fig = make_subplots(rows=1, cols=3, 
                    specs=[[{'type': 'scatter3d'}, {'type': 'scatter3d'}, {'type': 'scatter3d'}]],
                    subplot_titles=('Pure Fibonacci', 'Pure Saff-Kuijlaars', 'Hybrid (Saff-Poles + Fibo-Equator)'))

algos = [fibo_algo, saff_algo, hybrid_algo]

for i, algo in enumerate(algos):
    pts = algo(n_points)
    
    # We will color points based on latitude to show the transition
    colors = []
    transition_z = np.sin(np.radians(60.0))
    for pt in pts:
        if np.abs(pt[2]) >= transition_z:
            colors.append('#EF553B') # Red for polar region
        else:
            colors.append('#636EFA') # Blue for equatorial region
            
    fig.add_trace(go.Scatter3d(x=pts[:,0], y=pts[:,1], z=pts[:,2],
                               mode='markers', marker=dict(size=3, color=colors)),
                  row=1, col=i+1)

fig.update_layout(height=600, width=1000, title_text=f"Distribution Visualizations for N={n_points}", showlegend=False)
fig.show()"""),

    nbf.v4.new_markdown_cell("## Metric Benchmarking\nComparing the global performance metrics of the pure algorithms versus the hybrid model."),

    nbf.v4.new_code_cell("""n_values = [500, 1000, 2000, 3000]
results = []

algos_dict = {
    'Fibonacci': fibo_algo,
    'Saff-Kuijlaars': saff_algo,
    'Hybrid (Saff/Fibo @ 60deg)': hybrid_algo
}

for n in n_values:
    for name, algo in algos_dict.items():
        pts = algo(n)
        min_dist, max_dist, std_dev = analyze_points(pts)
        results.append({
            'N': n,
            'Algorithm': name,
            'Min Dist': min_dist,
            'Max Dist': max_dist,
            'Max - Min Dist': max_dist - min_dist,
            'Std Dev': std_dev
        })

df = pd.DataFrame(results)
display(df)"""),

    nbf.v4.new_markdown_cell("## Topographical Analysis\nObserving the Standard Deviation across latitudinal bins to verify if the hybrid algorithm successfully combines the strengths of both parent algorithms."),

    nbf.v4.new_code_cell("""n_eval = 2000
lat_results = []

for name, algo in algos_dict.items():
    pts = algo(n_eval)
    bins = latitudinal_analysis(pts, num_bins=18)
    for b in bins:
        b['Algorithm'] = name
    lat_results.extend(bins)

lat_df = pd.DataFrame(lat_results)

fig = go.Figure()
algo_colors = {'Fibonacci': '#636EFA', 'Saff-Kuijlaars': '#EF553B', 'Hybrid (Saff/Fibo @ 60deg)': '#00CC96'}

for name in algos_dict.keys():
    subset = lat_df[lat_df['Algorithm'] == name]
    color = algo_colors.get(name, '#333333')
    fig.add_trace(go.Scatter(x=subset['latitude_deg'], y=subset['std_dev'], 
                             mode='lines+markers', name=name, line=dict(color=color)))

# Add vertical lines to denote the 60 degree transitions
fig.add_vline(x=60, line_dash="dash", line_color="black", annotation_text="Transition Boundary")
fig.add_vline(x=-60, line_dash="dash", line_color="black")

fig.update_layout(title=f"Standard Deviation of Distances by Latitude (N={n_eval})",
                  xaxis_title="Latitude (degrees)",
                  yaxis_title="Standard Deviation", height=500)
fig.show()""")
]

with open('Hybrid_Algorithm_Study.ipynb', 'w') as f:
    nbf.write(nb, f)
