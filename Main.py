import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
from urllib.request import urlopen
import requests
import ssl
import json
import numpy as np
import pydeck as pdk

ssl._create_default_https_context = ssl._create_unverified_context

st.markdown("<h1 style='color:#8C2F39; text-align:center;'>Visualización de datos históricos del catálogo sísmico Perú</h1> <br><br>", unsafe_allow_html=True)

# Cargar datos de URL y convertir a DataFrame
# @st.cache_data # este decorador permite almacenar en caché los datos para evitar recargas innecesarias
def load_data(url, type='csv', file_name='temp'):
    # Cabeceras para la solicitud
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        "Accept-Language": "en-US,en;q=0.9",
    }

    # Realizar la solicitud
    req = urllib.request.Request(url, headers=headers, method='GET')

    # Descargar el archivo
    with urlopen(req) as response, open(file_name, 'wb') as out_file:
        out_file.write(response.read())

    # Leer el archivo según su tipo
    if type == 'csv':
        return pd.read_csv(file_name)
    elif type == 'xlsx':
        return pd.read_excel(file_name)
    elif type == 'json':
        with open(file_name, 'r') as file:
            data = json.load(file)
        return pd.DataFrame(data)
    else:
        raise ValueError("Unsupported file type")
    
#Clasificación de profundidad
def get_profundidad_category(profundidad):
    if profundidad <= 70:
        return "Superficiales"
    elif profundidad <= 450:
        return "Intermedios"
    return "Profundos"

#Procesamiento de datos
def process_data(df):
    # Eliminar columnas innecesarias
    df.drop(columns=['FECHA_CORTE'], inplace=True)

    # Renombrar columnas
    df.rename(columns={
        'FECHA_UTC': 'Fecha',
        'HORA_UTC': 'Hora',
        'LATITUD': 'latitude',
        'LONGITUD': 'longitude',
        'MAGNITUD': 'Magnitud',
        'PROFUNDIDAD': 'Profundidad',
    }, inplace=True)

    # Convertir columnas a tipos adecuados
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce', format='%Y%m%d')
    df['Hora'] = pd.to_datetime(df['Hora'], errors='coerce', format='%H%M%S').dt.time
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df['Magnitud'] = pd.to_numeric(df['Magnitud'], errors='coerce')
    df['Profundidad'] = pd.to_numeric(df['Profundidad'], errors='coerce')
    df["TipoProfundidad"] = df["Profundidad"].transform(get_profundidad_category)

    return df

# Main para mostrar los datos
if __name__ == "__main__":
    url = "https://www.datosabiertos.gob.pe/sites/default/files/Catalogo1960_2023.xlsx"
    df = load_data(url, type='xlsx', file_name='earthquakes.xlsx')
    df = process_data(df)
    # Imprimir dataframe en consola
    print(df.head())


#Sidebar para los filtros del dataset
st.sidebar.title("Filtros")

max_fecha = df['Fecha'].max()
min_fecha = max_fecha - pd.DateOffset(years=1)

fecha_range = st.sidebar.date_input("Rango de fechas", [min_fecha, max_fecha])

magnitud_range = st.sidebar.slider("Magnitud", float(df['Magnitud'].min()), float(df['Magnitud'].max()), (2.5, 4.9))
profundidad_range = st.sidebar.slider("Profundidad (km)", float(df['Profundidad'].min()), float(df['Profundidad'].max()), (0.0, 200.0))

#Aplicar filtros
df_filtrado = df[
    (df['Fecha'] >= pd.to_datetime(fecha_range[0])) &
    (df['Fecha'] <= pd.to_datetime(fecha_range[1])) &
    (df['Magnitud'] >= magnitud_range[0]) &
    (df['Magnitud'] <= magnitud_range[1]) &
    (df['Profundidad'] >= profundidad_range[0]) &
    (df['Profundidad'] <= profundidad_range[1])
]

#Distribución de magnitud por frecuencia
def distribution_frecuency(df_filtrado):
    st.markdown("""
        <p style='font-size: 1.1rem; color:#461220'>
        El 90% de los sismos tiene magnitud < 5.5</p> <br>""", unsafe_allow_html=True)
    plt.figure(figsize=(6,4))
    plt.hist(df_filtrado['Magnitud'], bins=40, color='#FCB9B2')
    plt.xlabel("Magnitud")
    plt.ylabel("Frecuencia")
    st.pyplot(plt.gcf())

#Distribución de masgnitud por profundidad
def distribution_profundity(df_filtrado):
    st.markdown("""
        <p style='font-size: 1.1rem; color:#461220'>
        La profundidad entre 50 y 150 km confirma un régimen tectónico de subducción activo</p>""", unsafe_allow_html=True)
    plt.figure(figsize=(6,4))
    plt.scatter(df_filtrado['Magnitud'], df_filtrado['Profundidad'], alpha=0.5, c='#FCB9B2', marker='.')
    plt.xlabel("Magnitud")
    plt.ylabel("Profundidad (km)")
    st.pyplot(plt.gcf())

#Mapa del perú con puntos de referencia segun la latitud y longitud de los sismos
def map_lat_long(df_filtrado):
    st.markdown("""
        <p style='font-size: 1.1rem; color:#461220'>
        La costa peruana es sísmicamente activa de forma generalizada</p>""", unsafe_allow_html=True)
    st.map(df_filtrado, latitude=df_filtrado['latitude'], longitude=df_filtrado['longitude'], color='#B23A48')

#Listado de cantidad de sismos por año
def frame_cantidad_sismos(df_filtrado):
    st.markdown("""
        <p style='font-size: 1.1rem; color:#461220'>
        La actividad sísmica reportada aumentó notablemente después del año 2000, coincidiendo con la modernización del sistema de monitoreo</p>""", unsafe_allow_html=True)
    df_filtrado["Year"] = pd.to_datetime(df_filtrado["Fecha"], format='%Y%m%d').dt.year
    df2 = df_filtrado.groupby("Year").size().reset_index(name="Count")
    st.dataframe(df2, hide_index=True, column_config={"Year": "Año", "Count": "Cantidad"})

#Listado de cantidad sismos por profundidad
def frame_tipo_profundidad(df_filtrado):
    st.markdown("""
        <p style='font-size: 1.1rem; color:#461220'>
        Gran porcentaje de los sismos son eventos clasificados como superficiales y deben ser prioridad para la planificación urbana y protección civil</p>""", unsafe_allow_html=True)
    
    df2 = df_filtrado.groupby("TipoProfundidad").size().reset_index(name="COUNT")
    st.dataframe(df2, hide_index=True, column_config={"TipoProfundidad": "Tipo de profundidad", "COUNT": "Cantidad"})

#Distribución de gráficos y tablas
col1, col2 = st.columns(2)

with col1:
    distribution_frecuency(df_filtrado)

with col2:
    distribution_profundity(df_filtrado)

col3, col4 = st.columns(2)

with col3:
    frame_cantidad_sismos(df_filtrado)

with col4:
    frame_tipo_profundidad(df_filtrado)

map_lat_long(df_filtrado)