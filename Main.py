import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
from urllib.request import urlopen
import requests
import ssl
import json
ssl._create_default_https_context = ssl._create_unverified_context

# Cargar datos de URL y convertir a DataFrame
@st.cache_data # este decorador permite almacenar en caché los datos para evitar recargas innecesarias
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

def process_data(df):
    # Eliminar columnas innecesarias
    df.drop(columns=['ID', 'FECHA_CORTE'], inplace=True)

    # Renombrar columnas
    df.rename(columns={
        'FECHA_UTC': 'Fecha',
        'HORA_UTC': 'Hora',
        'LATITUD': 'Latitud',
        'LONGITUD': 'Longitud',
        'MAGNITUD': 'Magnitud',
        'PROFUNDIDAD': 'Profundidad',
    }, inplace=True)

    # Convertir columnas a tipos adecuados
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce', format='%Y%m%d')
    df['Hora'] = pd.to_datetime(df['Hora'], errors='coerce', format='%H%M%S').dt.time
    df['Latitud'] = pd.to_numeric(df['Latitud'], errors='coerce')
    df['Longitud'] = pd.to_numeric(df['Longitud'], errors='coerce')
    df['Magnitud'] = pd.to_numeric(df['Magnitud'], errors='coerce')
    df['Profundidad'] = pd.to_numeric(df['Profundidad'], errors='coerce')

    return df

# Main para mostrar los datos
if __name__ == "__main__":
    url = "https://www.datosabiertos.gob.pe/sites/default/files/Catalogo1960_2023.xlsx"
    df = load_data(url, type='xlsx', file_name='earthquakes.xlsx')
    df = process_data(df)
    # Imprimir dataframe en consola
    print(df.head())