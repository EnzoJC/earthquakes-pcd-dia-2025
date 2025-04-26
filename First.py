import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from Second import tendencia_sismos_tiempo, sismos_por_departamento
from Third import third

## Graficos y tablas para la primera página
# @author: Kattya Garcia
def first(df):
    # Sidebar para los filtros del dataset
    st.sidebar.title("Filtros")

    max_fecha = df['date'].max()
    min_fecha = max_fecha - pd.DateOffset(years=20)

    fecha_range = st.sidebar.date_input("Rango de fechas", [min_fecha, max_fecha])

    magnitud_range = st.sidebar.slider("Magnitud", float(df['magnitude'].min()), float(df['magnitude'].max()+5),
                                       (2.5, 7.9))
    profundidad_range = st.sidebar.slider("Profundidad (km)", float(df['depth'].min()), float(df['depth'].max()+300),
                                          (0.0, 500.0))

    # Aplicar filtros
    df_filtrado = df[
        (df['date'] >= pd.to_datetime(fecha_range[0])) &
        (df['date'] <= pd.to_datetime(fecha_range[1])) &
        (df['magnitude'] >= magnitud_range[0]) &
        (df['magnitude'] <= magnitud_range[1]) &
        (df['depth'] >= profundidad_range[0]) &
        (df['depth'] <= profundidad_range[1])
        ]
    st.markdown("""
        <h2 style='color:#31333F; text-align:center;'>
        Análisis de sismos en el Perú</h2>
        """, unsafe_allow_html=True)
    tendencia_sismos_tiempo(df_filtrado)
    st.markdown("<div class='section-margin' style='padding: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        distribution_frequency(df_filtrado)
        st.markdown("<div class='section-margin' style='padding: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
        sismos_por_departamento(df_filtrado)
    with col2:
        distribution_profundity(df_filtrado)
        st.markdown("<div class='section-margin' style='padding: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
        third(df_filtrado)
    st.markdown("<div class='section-margin' style='padding: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
    map_lat_long(df_filtrado)

# Distribución de magnitud por frecuencia
def distribution_frequency(df_filtrado):

    st.markdown("""
        <p style='font-size: 1.1rem; color:#461220'>
        El 90% de los sismos tiene magnitud < 5.5</p>
        """,unsafe_allow_html=True)
    plt.figure(figsize=(6, 4), facecolor='#F0F2F6')
    ax = plt.gca()
    ax.set_facecolor("#F0F2F6")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#312F2F')
    ax.spines['left'].set_color('#312F2F')
    ax.tick_params(axis='x', colors='#312F2F')
    ax.tick_params(axis='y', colors='#312F2F')
    plt.hist(df_filtrado['magnitude'], bins=25, color='#FF4B4B')
    plt.xlabel("Magnitud")
    plt.ylabel("Cantidad")
    st.pyplot(plt.gcf())


# Distribución de masgnitud por profundidad
def distribution_profundity(df_filtrado):
    st.markdown("""
        <p style='font-size: 1.1rem; color:#461220'>
        Los sismos más poderosos tienden a ocurrir a menor profundidad.</p>""",
                unsafe_allow_html=True)
    plt.figure(figsize=(6, 4), facecolor='#F0F2F6')
    ax = plt.gca()
    ax.set_facecolor("#F0F2F6")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#312F2F')
    ax.spines['left'].set_color('#312F2F')
    ax.tick_params(axis='x', colors='#312F2F')
    ax.tick_params(axis='y', colors='#312F2F')
    plt.scatter(df_filtrado['depth'], df_filtrado['magnitude'], alpha=0.5, c='#FF4B4B', marker='.')
    plt.xlabel("Profundidad (km)")
    plt.ylabel("Magnitud")
    st.pyplot(plt.gcf())


# Mapa del perú con puntos de referencia segun la latitud y longitud de los sismos
def map_lat_long(df_filtrado):
    st.markdown("""
        <p style='font-size: 1.1rem; color:#461220'>
        La costa peruana es sísmicamente activa de forma generalizada</p>""", unsafe_allow_html=True)
    st.map(df_filtrado, latitude=df_filtrado['latitude'], longitude=df_filtrado['longitude'], color='#B23A48')


# # Listado de cantidad de sismos por año
# def frame_cantidad_sismos(df_filtrado):
#     st.markdown("""
#         <p style='font-size: 1.1rem; color:#461220'>
#         La actividad sísmica reportada aumentó notablemente después del año 2000, coincidiendo con la modernización del sistema de monitoreo</p>""",
#                 unsafe_allow_html=True)
#     df_filtrado["Year"] = pd.to_datetime(df_filtrado["date"], format='%Y%m%d').dt.year
#     df2 = df_filtrado.groupby("Year").size().reset_index(name="Count")
#     st.dataframe(df2, hide_index=True, column_config={"Year": "Año", "Count": "Cantidad"})
#
#
# # Listado de cantidad sismos por profundidad
# def frame_tipo_profundidad(df_filtrado):
#     st.markdown("""
#         <p style='font-size: 1.1rem; color:#461220'>
#         Gran porcentaje de los sismos son eventos clasificados como superficiales y deben ser prioridad para la planificación urbana y protección civil</p>""",
#                 unsafe_allow_html=True)
#
#     df2 = df_filtrado.groupby("depthType").size().reset_index(name="COUNT")
#     st.dataframe(df2, hide_index=True, column_config={"depthType": "Tipo de profundidad", "COUNT": "Cantidad"})
