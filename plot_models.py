# %%
# packages
from pathlib import Path
import nlmod
import sys
import folium as folium
import geopandas as gpd
# %%
# setup
model_names = [
    "example_model",
    "manteling",
]

gdf = gpd.GeoDataFrame(columns=["model", "type", "url", "geometry"])

# %%
# fill geodataframe
for model_name in model_names:
    model_ws = Path(f"../{model_name}/src")
    print(model_ws)
    sys.path.insert(0, str(model_ws))
    settings = __import__("settings")
    extent = list(settings.extent)

    gdf.loc[f"model extent {model_name}"] = [
        model_name,
        "extent",
        f"<a href=https://github.com/ZLFLO/{model_name.lower()} target='_blank'>{model_name}</a>",
        nlmod.util.extent_to_polygon(extent),
    ]
    print(extent)

    del sys.modules["settings"]
gdf = gdf.set_crs("EPSG:28992")
# %%
# plot geodataframe to double check
ax = gdf.plot(alpha=0.5)
nlmod.plot.add_background_map(ax=ax)
# %%
# create folium map and html file
gdf = gdf.to_crs("EPSG:4326")  # Convert to WGS84
fmap = gdf.explore(column="model", tooltip=["model", "type"], popup="url")
fmap.fit_bounds([[51.2, 3.35], [51.8, 4.3]])  # set extent to zeeland province
fmap.save("build/overview.html")
fmap
