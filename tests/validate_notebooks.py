"""Execute both notebook layouts in fresh kernels, including Part 2 on its own.

Run with: python tests/validate_notebooks.py
Requires: nbclient, nbformat, ipykernel (notebook setup installs its own packages).
Temporary copies keep generated pickles and outputs out of the source tree.
"""

from pathlib import Path
import shutil
import tempfile

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted(ROOT.glob("NB*.ipynb"))
CHECKS = """
import math
from numbers import Real

assert len(deaths_df) == 250
assert len(pumps_df) == 8
assert deaths_df['DEATHS'].sum() == 489
tiles = [layer for layer in map1._children.values()
         if isinstance(layer, folium.TileLayer)]
assert len(tiles) == 1
assert '/Canvas/World_Light_Gray_Base/MapServer/tile/' in tiles[0].tiles
assert tiles[0].options['attribution']
assert tiles[0].options['max_native_zoom'] == 16
assert tiles[0].options['max_zoom'] == 19
circles = [layer for layer in map1._children.values()
           if isinstance(layer, folium.CircleMarker)]
assert all(isinstance(layer.options['radius'], Real) for layer in circles)
assert len(circles) == 250 + (1 if 'mean_center_POINT' in globals() else 0)
assert len([layer for layer in map1._children.values()
            if isinstance(layer, folium.RegularPolygonMarker)]) == 8
if 'mean_center_POINT' in globals():
    assert math.isclose(mean_center_POINT[0], 51.51339831083845)
    assert math.isclose(mean_center_POINT[1], -0.1364029734151329)
    assert (OUTPUT_DIR / 'mean_center_df.pickle').is_file()
else:
    assert pd.read_pickle(OUTPUT_DIR / 'deaths_df.pickle').equals(deaths_df)
    assert pd.read_pickle(OUTPUT_DIR / 'pumps_df.pickle').equals(pumps_df)
map1.save('validated-map.html')
"""


def execute(path, directory):
    notebook = nbformat.read(path, as_version=4)
    notebook.cells.append(nbformat.v4.new_code_cell(CHECKS))
    NotebookClient(
        notebook, timeout=300, kernel_name="python3", allow_errors=False,
        resources={"metadata": {"path": str(directory)}},
    ).execute()
    print(f"PASS {path.relative_to(ROOT)} ({len(notebook.cells)} cells)", flush=True)


def main():
    for name in NOTEBOOKS:
        assert name.read_bytes() == (ROOT / "contents" / name.name).read_bytes()
    for layout in ("repository", "contents"):
        with tempfile.TemporaryDirectory(prefix=f"cholera-{layout}-") as scratch:
            directory = Path(scratch)
            source = ROOT if layout == "repository" else ROOT / "contents"
            resource_source = ROOT / "resources" if layout == "repository" else source
            resources = directory / "resources" if layout == "repository" else directory
            resources.mkdir(exist_ok=True)
            for name in ("library.py", "style.css", "cholera_deaths.csv", "pumps.csv"):
                shutil.copy2(resource_source / name, resources / name)
            # No output directory or Part 1 pickles exist at this point.
            execute(source / NOTEBOOKS[1].name, directory)
            execute(source / NOTEBOOKS[0].name, directory)
            # A new kernel now reads the Part 1 pickles.
            execute(source / NOTEBOOKS[1].name, directory)


if __name__ == "__main__":
    main()
