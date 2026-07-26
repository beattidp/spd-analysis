# Proposal and Implementation Plan: Spherical Point Distribution Analysis

This document outlines the proposal and phased implementation plan for analyzing and comparing algorithms that distribute $N$ points on a sphere.

## User Review Required

> [!IMPORTANT]
> Please review the two selected "preferred algorithms" (Fibonacci Lattice and Saff-Kuijlaars Spiral) and confirm if they meet your requirements, or if you prefer other algorithms (e.g., Thomson Problem simulation, Random distribution, Golden Spiral).
> Also, confirm the proposed range of $N$ (e.g., $N=10$ to $N=5,000$) for the metric analysis.

## Visualization Components & Rationale

- **3D Visualization**: We will use **Plotly** (`plotly.graph_objects`) for 3D visualization. 
  - **Rationale**: Plotly supports interactive, browser-based 3D plots natively in Jupyter notebooks. We can create side-by-side synchronized subplots (e.g., 1x3 grid), allowing you to rotate, pan, and zoom into one sphere and see the same perspective across all three algorithm models simultaneously.
- **Data Ranking & Summarization**: We will use **Pandas** to compile the metrics (min distance, max distance, standard deviation).
  - **Rationale**: Pandas offers built-in sorting, ranking, and display capabilities perfect for tabular data in a Jupyter notebook.
- **Topological/Latitudinal Analysis**: We will segment the sphere into latitudinal bands and visualize the standard deviation within those bands using 2D line charts or heatmaps.

---

## Phase 1: Environment Setup

- Create a `virtualenv` in `~/lang/python3/antigravity/spd-analysis` using the default Python version reported by pyenv (3.13.1).
- Install the Jupyter engine and necessary dependencies:
  - `jupyterlab`, `notebook`
  - `numpy`, `scipy` (for spatial KDTree distance calculations)
  - `pandas` (for analysis and ranking)
  - `plotly` (for 3D visualization)

## Phase 2: Algorithm Implementation

We will implement three algorithms to generate the coordinates of $N$ points on a unit sphere (radius = 1):
1. **Fibonacci Lattice**: A standard analytical method using the Golden Ratio, widely used for near-uniform distribution.
2. **Saff-Kuijlaars Spiral**: A highly efficient spiral method that produces an asymptotically uniform distribution.
3. **Kogan (2017)**: The computationally efficient method introduced by Jonathan Kogan for spacing $n$ points on a sphere, which achieves 70%-86% accuracy of theoretical bounds.

## Phase 3: Metrics & Analytical Framework

For each algorithm and each $N$ across the predefined range (e.g., starting at 10 up to 5,000+ points), we will calculate:
- **Minimum Distance**: The absolute minimum Euclidean (or spherical) distance between any two points.
- **Maximum Distance**: The maximum of the nearest-neighbor distances for all points.
- **Standard Deviation**: The standard deviation of all nearest-neighbor distances.

**Latitudinal Analysis**:
- Group points into latitudinal bins (e.g., 10-degree increments from pole to pole).
- Calculate the deviation/density in each region to identify where the greatest shifts or irregularities occur for each algorithm.

## Phase 4: Jupyter Notebook Generation

- Assemble the implementation into a structured, readable Jupyter Notebook (`Spherical_Point_Distribution_Analysis.ipynb`).
- Add the ranking facility: A function that takes a given $N$ and ranks the algorithms from best to worst based on minimum deviation and tightest distance bounds.
- Add practical guidance and switching logic: Suggest threshold values of $N$ or specific latitudes where one algorithm outperforms the others.
- Render the side-by-side 3D visualization.

---

## Verification Plan

### Automated / Programmatic Tests
- Verify that `pyenv` and `venv` correctly initialize the environment.
- Programmatically assert that all algorithms output exactly $N$ points on the unit sphere ($x^2 + y^2 + z^2 = 1$).
- Ensure that distance calculations utilizing `scipy.spatial.cKDTree` are correctly parameterized for nearest neighbors.

### Manual Verification
- Review the Jupyter Notebook visualizations to ensure Plotly subplots render side-by-side effectively.
- Verify the ranking tables are clearly formatted.
