import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def fourth(df):
    # Sidebar para los filtros del dataset
    st.sidebar.title("Filtros")

    max_fecha = df['date'].max()
    min_fecha = max_fecha - pd.DateOffset(years=1)

    fecha_range = st.sidebar.date_input("Rango de fechas", [min_fecha, max_fecha])

    magnitud_range = st.sidebar.slider("Magnitud", float(df['magnitude'].min()), float(df['magnitude'].max()),
                                       (2.5, 4.9))
    profundidad_range = st.sidebar.slider("Profundidad (km)", float(df['depth'].min()), float(df['depth'].max()),
                                          (0.0, 200.0))

    # Aplicar filtros
    df_filtrado = df[
        (df['date'] >= pd.to_datetime(fecha_range[0])) &
        (df['date'] <= pd.to_datetime(fecha_range[1])) &
        (df['magnitude'] >= magnitud_range[0]) &
        (df['magnitude'] <= magnitud_range[1]) &
        (df['depth'] >= profundidad_range[0]) &
        (df['depth'] <= profundidad_range[1])
        ]