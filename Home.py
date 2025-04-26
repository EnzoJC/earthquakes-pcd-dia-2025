import streamlit as st

## Página de inicio
# @author: Anlly Correa
def home_page(df):

    st.markdown("""
        <style>
        .main-title { color: #1E3A8A; text-align: center; font-size: 2.5em; font-weight: bold; margin-bottom: 20px; }
        .subheader { color: #4B5563; font-size: 1.5em; font-weight: 600; margin-top: 30px; margin-bottom: 15px; }
        .info-box { background-color: #F3F4F6; padding: 20px; border-radius: 10px; margin: 20px 0; }
        .highlight { color: #DC2626; font-weight: bold; }
        .btn-explore { 
            background-color: #60A5FA; 
            color: white; 
            padding: 12px 24px; 
            border-radius: 8px; 
            text-align: center; 
            display: inline-block; 
            text-decoration: none; 
            font-size: 1.1em; 
        }
        .btn-explore:hover { background-color: #1E3A8A; }
        .section-margin { margin-top: 40px; margin-bottom: 40px; }
        .center-text { text-align: center; }
        .italic-quote { font-style: italic; color: #4B5563; }
        .motivational-text { font-size: 1.2em; color: #1E3A8A; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)


    st.markdown("""
        <h1 class='main-title'>Catálogo Sísmico del Perú 1960-2023 🌍</h1>
        <p class='center-text' style='color:#4B5563; margin-bottom: 30px;'>
            Explora la actividad sísmica registrada por el <span class='highlight'>Instituto Geofísico del Perú (IGP)</span>
        </p>
    """, unsafe_allow_html=True)


    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
            <h2 class='subheader'>¿Qué es un sismo? ⚡</h2>
            <p>
                Un sismo es una sacudida de la Tierra causada por el movimiento de las placas tectónicas. 
                Gracias a la <b>tomografía sísmica</b>, los sismos nos revelan el interior de nuestro planeta.
            </p>
            <p><b>Causas principales</b>:</p>
            <ul>
                <li>🏔️ <b>Tectónica</b>: Desplazamiento de placas, la más común.</li>
                <li>🌋 <b>Volcánica</b>: Erupciones violentas, menos frecuentes.</li>
                <li>🕳️ <b>Hundimientos</b>: Erosión subterránea, alcance limitado.</li>
                <li>🪨 <b>Deslizamientos</b>: Movimientos en fallas.</li>
                <li>💥 <b>Humanas</b>: Explosiones atómicas.</li>
            </ul>
        """, unsafe_allow_html=True)
    
    with col2:
        st.image("https://www.chiquianmarka.com/uploads/3/9/2/8/39281031/published/terremoto-1.jpg?1589807696", caption="Terremoto del 31 de Mayo de 1970 🌎", use_container_width=True)

 
    st.markdown("""
        <div class='info-box section-margin'>
            <h2 class='subheader'>El Perú: En el corazón del Cinturón de Fuego 📍</h2>
            <p>
                El Perú, ubicado en el <span class='highlight'>Cinturón de Fuego del Pacífico</span>, es una de las regiones más sísmicas del mundo. 
                Eventos históricos como el sismo de Áncash (1970) dejaron miles de víctimas y enseñaron la importancia de la preparación. 
                La autoconstrucción y viviendas antiguas aumentan la vulnerabilidad, haciendo crucial el estudio de los sismos.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col3, col4 = st.columns([2, 1])
    
    with col3:
        st.markdown("""
            <h2 class='subheader'>El Catálogo Sísmico 1960-2021 📊</h2>
            <p>
                Elaborado por el <span class='highlight'>IGP</span>, este catálogo registra todos los sismos percibidos en el Perú desde 1960. 
                Incluye datos clave como:
            </p>
            <ul>
                <li>📅 Fecha y hora del sismo.</li>
                <li>📏 Magnitud y profundidad.</li>
                <li>🌐 Latitud, longitud y ubicación.</li>
            </ul>
            <p>
                Estos datos son ideales para:
            </p>
            <ul>
                <li>🔍 Análisis sismológico.</li>
                <li>🛡️ Planificación de prevención.</li>
                <li>📚 Educación pública.</li>
            </ul>
            <p><b>Dato curioso</b>: ¡El Perú registra un promedio de 3 sismos perceptibles por semana!</p>
            <p>
                📂 Descarga el dataset completo aquí: 
                <a href='https://www.datosabiertos.gob.pe/dataset/catalogo-sismico-1960-2021-igp' target='_blank' style='color:#60A5FA; text-decoration:underline;'>Catálogo Sísmico 1960-2021 (IGP)</a>
            </p>
        """, unsafe_allow_html=True)
    

    with col4:
        st.markdown("""
            <h2 class='subheader'>Explora los datos sísmicos 🔍</h2>
            <p>Visualiza mapas, filtra eventos y descubre la historia sísmica del Perú.</p>
        """, unsafe_allow_html=True)
        if st.button("¡Comienza ahora! 🚀", key="explore_button"):
            st.write("¡Dirigiéndote a la sección de visualización de datos!")

    st.markdown("</div>", unsafe_allow_html=True)

    st.dataframe(df)

    st.markdown("""
        <div class='section-margin center-text motivational-text'>
            ¡Descubre los secretos de la Tierra y ayuda a construir un Perú más preparado! 🌟
        </div>
    """, unsafe_allow_html=True)
