#%%
from pathlib import Path
import nlmod
import sys
import folium as folium
import geopandas as gpd
#%%

model_names = [
    "example_model",
    "manteling",
]

gdf = gpd.GeoDataFrame(columns=["model", "type", "url", "geometry"])

def get_url_from_ml_name(model_name: str) -> str:
    url = f"<a href=https://github.com/ZLFLO/{model_name.lower()} target='_blank'>{model_name}</a>"
    return url

#%%
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
        get_url_from_ml_name(model_name),
        nlmod.util.extent_to_polygon(extent),
    ]
    print(extent)

    del sys.modules["settings"]
gdf = gdf.set_crs("EPSG:28992")
#%%
ax = gdf.plot(alpha=0.5)
nlmod.plot.add_background_map(ax=ax)
#%%
# create html file
fmap = gdf.explore(column="model", tooltip=["model", "type"], popup="url")
fmap.save("build/overview.html")
fmap