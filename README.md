# Jupyterlite-1854-Cholera-Basic
This is the Jupyterlite adaptation of our 1854-Cholera Basic case study.

Link to JupyterLite case study: https://phi-case-studies.github.io/Jupyterlite-1854-Cholera-Basic

Open either notebook and run all cells from top to bottom. Run the first setup cell
again after restarting the kernel. It uses `%pip`, which installs packages in both
JupyterLite's Pyodide kernel and regular Jupyter kernels. Internet access is needed
for the initial package downloads and the light grey basemap tiles.

The notebooks use `Esri.WorldGrayCanvas` because [CARTO now requires an API
key](https://carto.com/basemaps/apikey/). The Esri raster layer includes attribution
and scales its zoom-16 tiles at closer zoom levels to avoid missing-tile requests.

Part 2 reads Part 1's saved dataframes when present and otherwise loads the bundled
CSV files, so it can also run independently. Both notebooks create their `outputs/`
directory automatically. The repository-root and `contents/` notebook copies are
kept in sync and support their respective resource layouts.

To validate both notebooks in fresh local kernels, including Part 2 before and
after Part 1:

```sh
python -m pip install nbclient nbformat ipykernel
python tests/validate_notebooks.py
```

The validation executes temporary copies, checks the data and mean center, and
verifies that the maps have one Esri World Light Gray Canvas layer, valid zoom
limits, and numeric marker radii.
