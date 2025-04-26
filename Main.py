import streamlit as st
import pandas as pd
import urllib.request
import ssl
import json

from urllib.request import urlopen
from streamlit_option_menu import option_menu
from Home import home_page
from First import first

ssl._create_default_https_context = ssl._create_unverified_context

# Configuración de Streamlit
st.set_page_config(
    page_title="Earthquakes Data",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Cargar datos de URL y convertir a DataFrame
@st.cache_data  # este decorador permite almacenar en caché los datos para evitar recargas innecesarias
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

# Clasificación de profundidad
def get_profundidad_category(profundidad):
    if profundidad <= 70:
        return "Superficiales"
    elif profundidad <= 450:
        return "Intermedios"
    return "Profundos"

# Procesamiento de datos
def process_data(df):
    # Eliminar columnas innecesarias
    df.drop(columns=['ID', 'FECHA_CORTE'], inplace=True)

    # Renombrar columnas
    df.rename(columns={
        'FECHA_UTC': 'date',
        'HORA_UTC': 'time',
        'LATITUD': 'latitude',
        'LONGITUD': 'longitude',
        'MAGNITUD': 'magnitude',
        'PROFUNDIDAD': 'depth',
    }, inplace=True)

    # Convertir columnas a tipos adecuados
    df['date'] = pd.to_datetime(df['date'], errors='coerce', format='%Y%m%d')
    df['time'] = pd.to_datetime(df['time'], errors='coerce', format='%H%M%S').dt.time
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df['magnitude'] = pd.to_numeric(df['magnitude'], errors='coerce')
    df['depth'] = pd.to_numeric(df['depth'], errors='coerce')
    df["depthType"] = df["depth"].transform(get_profundidad_category)

    return df

def setup(df):
    # Sidebar date input
    with st.sidebar:
        selected = option_menu(
            menu_title="Earthquakes",
            options=["Principal", "Análisis"],
            icons=["house", "bar-chart"],
            menu_icon="globe-americas",
            default_index=0,
        )
    # Mostrar la página de inicio o las visualizaciones según la selección
    match selected:
        case "Principal":
            home_page(df)
        case "Análisis":
            first(df)

# Función principal
def main():
    # Cargar y procesar datos
    url = "https://www.datosabiertos.gob.pe/sites/default/files/Catalogo1960_2023.xlsx"
    df = load_data(url, type='xlsx', file_name='earthquakes.xlsx')
    df = process_data(df)

    # Cargar el dashboard con el DataFrame procesado
    setup(df)

if __name__ == "__main__":
    main()
