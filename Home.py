import streamlit as st
## Pagina de inicio
# @author: Kattya Garcia
def home_page():
    st.markdown("<h1 style='color:#8C2F39; text-align:center;'>Catálogo Sísmico 1960 - 2023</h1>",
                unsafe_allow_html=True)

    # Introducción al tema
    st.markdown(
        """
        ### ¿Qué es un sismo?
        Un sismo o un terremoto es un fenómeno natural que consiste en una sacudida de la superficie terrestre, producida por el movimiento de las capas interiores de la Tierra.
    
        Son de corta duración e intensidad variable y son producidos a consecuencia de la liberación repentina de energía. Paradójicamente, poseen un aspecto positivo que es el de proporcionarnos información sobre el interior de nuestro planeta. Actualmente, gracias a la técnica conocida como tomografía sismológica o sísmica, se conoce con gran detalle el interior de nuestro planeta.
        
        ### Causas:
                    
        Las causas más generales se pueden enumeran según su orden de importancia en:
                    
        - **TECTÓNICA**: son los sismos que se originan por el desplazamiento de las placas tectónicas que conforman la corteza, afectan grandes extensiones y es la causa que más genera sismos.
        - **VOLCÁNICA**: es poco frecuente; cuando la erupción es violenta genera grandes sacudidas que afectan sobre todo a los lugares cercanos, pero a pesar de ello su campo de acción es reducido en comparación con los de origen tectónico.
        - **HUNDIMIENTO**: cuando al interior de la corteza se ha producido la acción erosiva de las aguas subterráneas, va dejando un vacío, el cual termina por ceder ante el peso de la parte superior. Es esta caída que genera vibraciones conocidas como sismos. Su ocurrencia es poco frecuente y de poca extensión.
        - **DESLIZAMIENTOS**: el propio peso de las montañas es una fuerza enorme que tiende a aplanarlas y que puede producir sismos al ocasionar deslizamientos a lo largo de fallas, pero generalmente no son de gran magnitud.
        - **EXPLOSIONES ATÓMICAS**: realizadas por el ser humano y que al parecer tienen una relación con los movimientos sísmicos.
        
        El Perú, ubicado en el Cinturón de Fuego del Pacífico, es una región altamente sísmica. Esta actividad, combinada con un alto porcentaje de viviendas construidas mediante autoconstrucción o de antigüedad considerable, incrementa significativamente la vulnerabilidad de su población frente a eventos sísmicos. En este contexto, la plataforma de catálogo sísmico (1960-2023) nos brinda información relevante para el análisis detallado de los diversos datos e informar a los usuarios los sismos históricos en el pais.
    
        En esta página, puedes explorar datos sísmicos registrados desde 1960 hasta 2023. Usa la opción de gráfico del menú para visualizar mapas, datos y aplicar filtros personalizados según tus intereses.
        """
    )

    st.info(
        "La historia nos ha enseñado que los sismos pueden destruir, pero también pueden unirnos en la reconstrucción, en la innovación y en la esperanza de un futuro más seguro."
    )
