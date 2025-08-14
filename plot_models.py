from pathlib import Path
import nlmod
import sys

import geopandas as gpd

# load config from manteling model
manteling_ws = "../manteling/scripts"
sys.path.append(manteling_ws)
import config as manteling_config

sys.path.pop(len(sys.path) - 1)

# %%
gdf_models_overview = gpd.GeoDataFrame(columns=["model", "type", "geometry"])
gdf_models_overview.loc["model extent Manteling"] = [
    "Manteling",
    "model extent",
    nlmod.util.extent_to_polygon(manteling_config.extent),
]
gdf_models_overview.loc["interessegebied Manteling"] = [
    "Manteling",
    "interessegebied",
    manteling_config.shapes["manteling"],
]

gdf_models_overview["url"] = (
    "<a href=https://github.com/ZLFLO/"
    + gdf_models_overview["model"].str.lower()
    + ">"
    + gdf_models_overview["model"]
    + "</a>"
)
#%%
gdf_models_overview = gdf_models_overview.set_crs(epsg=28992)
m = gdf_models_overview.explore(column="model", tooltip=["model", "type"], popup="url")
m.save("build/figures/overview.html")

