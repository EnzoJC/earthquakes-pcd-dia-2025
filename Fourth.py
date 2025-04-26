import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium


def fourth(df):
    # Mapa de Calor para Perú resaltando ciudades/departamentos más afectados
    st.subheader("Mapa de Calor de Sismos en Perú")
    if not df.empty:
        center_lat = df['latitude'].mean()
        center_lon = df['longitude'].mean()
        heat_data = [[row['latitude'], row['longitude'], row['magnitude']]
                     for index, row in df.iterrows() if not pd.isnull(row['magnitude'])]

        map_ = folium.Map(location=[center_lat, center_lon], zoom_start=5)
        HeatMap(heat_data, radius=10, blur=15, max_zoom=1).add_to(map_)

        # Determinar ciudades o regiones con más sismos (aproximaciones por coordenadas)
        ciudades = {
            "Lima": (-12.0464, -77.0428),
            "Arequipa": (-16.4090, -71.5375),
            "Cusco": (-13.5319, -71.9675),
            "Trujillo": (-8.1118, -79.0288),
            "Ica": (-14.0678, -75.7286),
            "Puno": (-15.8402, -70.0219),
        }

        for ciudad, (lat, lon) in ciudades.items():
            nearby = df[(df['latitude'].between(lat - 1, lat + 1)) & (df['longitude'].between(lon - 1, lon + 1))]
            count = len(nearby)
            if count > 0:
                folium.Marker(
                    location=[lat, lon],
                    popup=f"{ciudad}: {count} sismos",
                    icon=folium.Icon(color='red' if count > 50 else 'orange', icon='info-sign')
                ).add_to(map_)

        st_folium(map_, width=700, height=500)
    else:
        st.warning("No se encontraron datos de sismos para Perú.")