import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
import webbrowser

gdf = gpd.read_file("datos.gpkg")  # O el archivo de cualquiera de los formatos

class MapaRegistros:
    def __init__(self, gdf):
        """
        Inicialización: recibe un GeoDataFrame con latitud, longitud y geometría.
        """
        self.gdf = gdf
        # Agrupar por ubicación (lat, long) para contar registros por ciudad
        self.puntos_agrupados = self.gdf.groupby(['lat', 'long']).size().reset_index(name='cantidad')

    def crear_mapa(self, ubicacion_inicial=[15, -85], zoom_inicial=1):
        """
        Crea un mapa mundial con folium centrado en la ubicación inicial
        """
        self.mapa = folium.Map(location=ubicacion_inicial,zoom_start=zoom_inicial,max_bounds=True,
                               min_zoom=3,   # Ajustar según el zoom más alejado deseado
                               max_zoom=10,  # Ajustar según el zoom más cercano deseado
                               width=600,height=600)
        self.mapa.fit_bounds([[-55.05, -81.8], [43.79, 4.32]])

        # Crear un clúster para manejar agrupación dinámica al hacer zoom
        marker_cluster = MarkerCluster().add_to(self.mapa)

        # Añadir puntos al mapa con tamaño proporcional a cantidad de registros
        for _, fila in self.puntos_agrupados.iterrows():
            lat = fila['lat']
            lon = fila['long']
            cantidad = fila['cantidad']
            # Radio proporcional (ejemplo: raíz cuadrada para mejor visual)
            radio = 3 * (cantidad ** 0.5)

            folium.CircleMarker(
                location=[lat, lon],
                radius=radio,
                #popup=f'Médicos: {int(cantidad)}',
                popup=folium.Popup(f'Médicos: {int(cantidad)}', parse_html=True),
                tooltip=f'Médicos: {int(cantidad)}',
                color='blue',
                fill=True,
                fill_color='blue',
                fill_opacity=0.6
            ).add_to(marker_cluster)

        return self.mapa
    

mapa_registros = MapaRegistros(gdf)
mapa_interactivo = mapa_registros.crear_mapa(ubicacion_inicial=[-15, -60], zoom_inicial=3)
mapa_interactivo.save("mapa_registros.html")
#webbrowser.open("mapa_registros.html")
