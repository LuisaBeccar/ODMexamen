
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Carga CSV con pandas
df = pd.read_csv("https://raw.githubusercontent.com/LuisaBeccar/ODMexamen/main/BaseODM2025g.csv")

# Crear geometría con puntos a partir de columnas de longitud y latitud de forma vectorizada
geometry = gpd.points_from_xy(df['long'], df['lat'])

# Crear GeoDataFrame usando la geometría generada
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Asignar CRS (WGS84)
gdf.set_crs(epsg=4326, inplace=True)

#Guardarlo en un archivo GeoPackage (.gpkg):
#Es un formato espacial estándar y recomendable porque guarda la geometría y atributos.
gdf.to_file("datos.gpkg", layer='datos', driver="GPKG")
