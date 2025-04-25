import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

## Graficos y tablas para la primera página
# @author: Kattya Garcia
def first(df):
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

    # Distribución de gráficos y tablas
    col1, col2 = st.columns(2)

    with col1:
        distribution_frequency(df_filtrado)

    with col2:
        distribution_profundity(df_filtrado)

    col3, col4 = st.columns(2)

    with col3:
        frame_cantidad_sismos(df_filtrado)

    with col4:
        frame_tipo_profundidad(df_filtrado)

    map_lat_long(df_filtrado)


# Distribución de magnitud por frecuencia
def distribution_frequency(df_filtrado):
    st.markdown("""
        <p style='font-size: 1.1rem; color:#461220'>
        El 90% de los sismos tiene magnitud < 5.5</p>""", unsafe_allow_html=True)
    plt.figure(figsize=(6, 4))
    plt.hist(df_filtrado['magnitude'], bins=40, color='#FCB9B2')
    plt.xlabel("Magnitud")
    plt.ylabel("Frecuencia")
    st.pyplot(plt.gcf())


# Distribución de masgnitud por profundidad
def distribution_profundity(df_filtrado):
    st.markdown("""
        <p style='font-size: 1.1rem; color:#461220'>
        La profundidad entre 50 y 150 km confirma un régimen tectónico de subducción activo</p>""",
                unsafe_allow_html=True)
    plt.figure(figsize=(6, 4))
    plt.scatter(df_filtrado['magnitude'], df_filtrado['depth'], alpha=0.5, c='#FCB9B2', marker='.')
    plt.xlabel("Magnitud")
    plt.ylabel("Profundidad (km)")
    st.pyplot(plt.gcf())


# Mapa del perú con puntos de referencia segun la latitud y longitud de los sismos
def map_lat_long(df_filtrado):
    st.markdown("""
        <p style='font-size: 1.1rem; color:#461220'>
        La costa peruana es sísmicamente activa de forma generalizada</p>""", unsafe_allow_html=True)
    st.map(df_filtrado, latitude=df_filtrado['latitude'], longitude=df_filtrado['longitude'], color='#B23A48')


# Listado de cantidad de sismos por año
def frame_cantidad_sismos(df_filtrado):
    st.markdown("""
        <p style='font-size: 1.1rem; color:#461220'>
        La actividad sísmica reportada aumentó notablemente después del año 2000, coincidiendo con la modernización del sistema de monitoreo</p>""",
                unsafe_allow_html=True)
    df_filtrado["Year"] = pd.to_datetime(df_filtrado["date"], format='%Y%m%d').dt.year
    df2 = df_filtrado.groupby("Year").size().reset_index(name="Count")
    st.dataframe(df2, hide_index=True, column_config={"Year": "Año", "Count": "Cantidad"})


# Listado de cantidad sismos por profundidad
def frame_tipo_profundidad(df_filtrado):
    st.markdown("""
        <p style='font-size: 1.1rem; color:#461220'>
        Gran porcentaje de los sismos son eventos clasificados como superficiales y deben ser prioridad para la planificación urbana y protección civil</p>""",
                unsafe_allow_html=True)

    df2 = df_filtrado.groupby("depthType").size().reset_index(name="COUNT")
    st.dataframe(df2, hide_index=True, column_config={"depthType": "Tipo de profundidad", "COUNT": "Cantidad"})
