import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# @author: Anlly Correa
def second(df):
    # Sidebar para los filtros del dataset
    st.sidebar.title("Filtros")

    # Ajustando el rango inicial para mostrar los últimos 10 años (2013-2023)
    max_fecha = df['date'].max()
    min_fecha = max_fecha - pd.DateOffset(years=10)

    fecha_range = st.sidebar.date_input("Rango de fechas", [min_fecha, max_fecha])

    magnitud_range = st.sidebar.slider("Magnitud", float(df['magnitude'].min()), float(df['magnitude'].max()),
                                       (2.5, 4.9))
    profundidad_range = st.sidebar.slider("Profundidad (km)", float(df['depth'].min()), float(df['depth'].max()),
                                          (0.0, 200.0))

    # filtros
    df_filtrado = df[
        (df['date'] >= pd.to_datetime(fecha_range[0])) &
        (df['date'] <= pd.to_datetime(fecha_range[1])) &
        (df['magnitude'] >= magnitud_range[0]) &
        (df['magnitude'] <= magnitud_range[1]) &
        (df['depth'] >= profundidad_range[0]) &
        (df['depth'] <= profundidad_range[1])
        ]

    with st.container():
        sismos_por_departamento(df_filtrado)


# Función para mapear coordenadas a departamentos de Perú
def map_to_departamento(lat, lon):
    # Rangos aproximados de latitud y longitud para cada departamento de Perú
    departamentos = {
        "Amazonas": {"lat_range": (-7.0, -2.0), "lon_range": (-78.5, -76.0)},
        "Áncash": {"lat_range": (-10.5, -8.5), "lon_range": (-78.0, -76.5)},
        "Apurímac": {"lat_range": (-14.5, -13.0), "lon_range": (-73.5, -71.5)},
        "Arequipa": {"lat_range": (-16.5, -15.0), "lon_range": (-72.5, -70.5)},
        "Ayacucho": {"lat_range": (-15.0, -12.0), "lon_range": (-74.5, -72.0)},
        "Cajamarca": {"lat_range": (-7.5, -4.5), "lon_range": (-79.0, -77.0)},
        "Callao": {"lat_range": (-12.1, -11.8), "lon_range": (-77.2, -76.9)},
        "Cusco": {"lat_range": (-15.0, -11.5), "lon_range": (-72.5, -70.0)},
        "Huancavelica": {"lat_range": (-14.0, -12.0), "lon_range": (-75.5, -74.0)},
        "Huánuco": {"lat_range": (-10.5, -8.0), "lon_range": (-76.5, -74.5)},
        "Ica": {"lat_range": (-15.5, -13.5), "lon_range": (-76.0, -74.5)},
        "Junín": {"lat_range": (-12.5, -10.5), "lon_range": (-76.0, -73.5)},
        "La Libertad": {"lat_range": (-9.0, -7.0), "lon_range": (-79.5, -77.5)},
        "Lambayeque": {"lat_range": (-7.0, -5.5), "lon_range": (-80.0, -79.0)},
        "Lima": {"lat_range": (-12.5, -10.5), "lon_range": (-77.5, -76.0)},
        "Loreto": {"lat_range": (-8.0, -0.5), "lon_range": (-77.0, -70.0)},
        "Madre de Dios": {"lat_range": (-13.5, -9.5), "lon_range": (-71.0, -68.5)},
        "Moquegua": {"lat_range": (-17.5, -16.5), "lon_range": (-71.5, -70.0)},
        "Pasco": {"lat_range": (-11.0, -9.5), "lon_range": (-76.5, -74.5)},
        "Piura": {"lat_range": (-6.5, -4.0), "lon_range": (-81.0, -79.0)},
        "Puno": {"lat_range": (-16.5, -13.5), "lon_range": (-71.0, -68.5)},
        "San Martín": {"lat_range": (-8.5, -5.5), "lon_range": (-77.5, -76.0)},
        "Tacna": {"lat_range": (-18.5, -17.0), "lon_range": (-71.0, -69.5)},
        "Tumbes": {"lat_range": (-4.5, -3.0), "lon_range": (-80.5, -79.5)},
        "Ucayali": {"lat_range": (-11.0, -7.5), "lon_range": (-75.0, -72.0)}
    }

    for dept, ranges in departamentos.items():
        lat_min, lat_max = ranges["lat_range"]
        lon_min, lon_max = ranges["lon_range"]
        if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
            return dept
    return "Desconocido"


# Gráfico de barras de cantidad de sismos por departamento
def sismos_por_departamento(df_filtrado):
    # st.markdown("""
    #     <h3 style='color:#31333F; text-align:center;'>
    #     Cantidad de Sismos por Departamento</h3>""", unsafe_allow_html=True)

    df_filtrado["Departamento"] = df_filtrado.apply(
        lambda row: map_to_departamento(row["latitude"], row["longitude"]), axis=1
    )

    df_grouped = df_filtrado.groupby("Departamento").size().reset_index(name="Count")

    df_grouped = df_grouped[df_grouped["Departamento"] != "Desconocido"]
    df_grouped = df_grouped.sort_values("Count", ascending=False).head(10)  # Top 10 departamentos

    max_dept = df_grouped.loc[df_grouped["Count"].idxmax()]
    st.markdown(f"<p style='font-size: 1.1rem; color:#461220'>El departamento de {max_dept['Departamento']} tuvo la mayor cantidad de sismos con un total de {max_dept['Count']} eventos.</p>",
                unsafe_allow_html=True)
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_grouped["Departamento"],
        y=df_grouped["Count"],
        marker_color='#FF4B4B',
        hovertemplate=
        '<b>Departamento</b>: %{x}<br>' +
        '<b>Cantidad de sismos</b>: %{y}<extra></extra>'
    ))

    fig.update_layout(
        xaxis_title="Departamento",
        yaxis_title="Cantidad de sismos",
        xaxis=dict(
            tickangle=45,
            showgrid=False,
            gridcolor='rgba(200, 200, 200, 0.2)',
            zeroline=False,
            title_font=dict(color='#461220', size=16),
            tickfont=dict(color='#461220', size=14)
        ),
        yaxis=dict(
            gridcolor='rgba(200, 200, 200, 0.2)',
            showgrid=False,
            zeroline=False,
            title_font=dict(color='#461220', size=16),
            tickfont=dict(color='#461220', size=14)
        ),
        plot_bgcolor='#F0F2F6',
        paper_bgcolor='#F0F2F6',
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False,
        shapes=[
            # Borde inferior
            dict(
                type="line",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=0,
                line=dict(color="#312F2F", width=1)
            ),
            # Borde izquierdo
            dict(
                type="line",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=0, y1=1,
                line=dict(color="#312F2F", width=1)
            )
        ],
    )

    st.plotly_chart(fig, use_container_width=True)


# Tendencia de sismos a lo largo del tiempo (frecuencia mensual) con interactividad
def tendencia_sismos_tiempo(df_filtrado):

    df_filtrado["YearMonth"] = pd.to_datetime(df_filtrado["date"]).dt.to_period('M')
    df_tendencia = df_filtrado.groupby("YearMonth").size().reset_index(name="Count")
    df_tendencia["YearMonth"] = df_tendencia["YearMonth"].dt.to_timestamp()

    df_filtrado["Year"] = pd.to_datetime(df_filtrado["date"]).dt.year
    avg_magnitude = df_filtrado.groupby("Year")["magnitude"].mean().reset_index()
    avg_magnitude["Year"] = avg_magnitude["Year"].astype(str)

    avg_magnitude_dict = dict(zip(avg_magnitude["Year"], avg_magnitude["magnitude"].round(2)))

    df_tendencia["Year"] = df_tendencia["YearMonth"].dt.year.astype(str)
    df_tendencia["AvgMagnitude"] = df_tendencia["Year"].map(avg_magnitude_dict)

    max_year = df_tendencia.loc[df_tendencia["Count"].idxmax()]
    insight = f"El año {int(max_year['Year'])} tuvo la mayor frecuencia de sismos con un total de {int(max_year['Count'])} eventos."
    st.markdown(f"<p style='font-size: 1.1rem; color:#461220'>{insight}</p>", unsafe_allow_html=True)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_tendencia["YearMonth"],
        y=df_tendencia["Count"],
        mode='lines',
        line=dict(color='#FF4B4B', width=2),
        hovertemplate=
        '<b>Fecha</b>: %{x|%Y-%m}<br>' +
        '<b>Cantidad de sismos</b>: %{y}<br>' +
        '<b>Promedio de magnitud (año)</b>: %{customdata}<extra></extra>',
        customdata=df_tendencia["AvgMagnitude"]
    ))

    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Cantidad de sismos",
        xaxis=dict(
            tickformat="%Y",
            tickangle=45,
            dtick="M12",
            showgrid=False,
            gridcolor='rgba(200, 200, 200, 0.2)',
            zeroline=False,
            title_font=dict(color='#461220', size=16),
            tickfont=dict(color='#461220', size=14)
        ),
        yaxis=dict(
            showgrid=False,
            gridcolor='rgba(200, 200, 200, 0.2)',
            zeroline=False,
            title_font=dict(color='#461220', size=16),
            tickfont=dict(color='#461220', size=14)
        ),
        plot_bgcolor='#F0F2F6',
        paper_bgcolor='#F0F2F6',
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False,

        shapes=[
            # Borde inferior
            dict(
                type="line",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=0,
                line=dict(color="#312F2F", width=1)
            ),
            # Borde izquierdo
            dict(
                type="line",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=0, y1=1,
                line=dict(color="#312F2F", width=1)
            )
        ]
    )

    st.plotly_chart(fig, use_container_width=True)
    #
    # st.markdown(
    #     f"""
    #     <div style="background-color:#FFFFFF; border:2px solid #d1d8e0; border-radius:10px; padding:10px; margin-top:15px; text-align:center; width:fit-content; margin-left:auto; margin-right:auto;">
    #         <p style="font-size:1rem; color:#461220; font-weight:bold; margin:0;">Insight Relevante</p>
    #         <p style="font-size:0.9rem; color:#461220; margin:0;">{insight}</p>
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )
