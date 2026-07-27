# Revision History & Changes

## v1.1.0 (Enhanced Continuous Evaluation)
* **Continuous Range Evaluation**: Enhanced the metric analysis pipeline to continuously benchmark algorithms across an unbroken range of point counts ($N=50$ to $N=2000$).
* **Ranking Transition Tracking**: Implemented dynamic identification of specific $N$ values where the ranking leader for Standard Deviation or Range flips. The main comparison table now exclusively populates using these precise topological transition thresholds.
* **Expanded Topographical Visualization**: Upgraded the latitudinal graphing capability. It now automatically extracts four noteworthy transition quantities from the continuous run and generates four separate, twin-subplot figures comparing Std Dev and Range.
* **Legend Styling Fixes**: Synchronized trace colors in Plotly across dual-axes to ensure one universal interactive legend per figure.

## v1.0.0 (Initial Stable Release)
* **Core Functionality**: Introduced a comparative benchmarking pipeline evaluating the Fibonacci Lattice, Saff-Kuijlaars Spiral, and Kogan (2017) point distribution algorithms.
* **3D & 2D Analytics**: Provided 3D Plotly visualization of distributed points and 2D charts evaluating standard deviation across discrete sample intervals (N = 50, 100, 250, 500, 1000, 2000, 5000).
* **Jupyter Integration**: Established an interactive Jupyter Notebook generated via `nbformat` rendering custom HTML/JS grouped tables.
* **Cloud Portability**: Included dynamic initialization hooks to support seamless cloning and execution directly inside Google Colaboratory.
