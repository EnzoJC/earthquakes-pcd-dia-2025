import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def third(df):
    # Los sismos superficiales no solo tienen mayor magnitud promedio, sino también una mayor variabilidad
    st.markdown("""
        <p style='font-size: 1.1rem; color:#461220'>
        Los sismos superficiales no solo tienen mayor magnitud promedio, sino también una mayor variabilidad.</p>""",
                unsafe_allow_html=True)
    custom_colors = ["#ff4b4b", "#fab1a8", "#ffe5de"]
    fig6, ax6 = plt.subplots(figsize=(6, 4), facecolor='#F0F2F6')
    sns.boxplot(data=df, x='depthType', y='magnitude', palette=custom_colors, ax=ax6)
    ax = plt.gca()
    ax.set_facecolor("#F0F2F6")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#312F2F')
    ax.spines['left'].set_color('#312F2F')
    ax.tick_params(axis='x', colors='#312F2F')
    ax.tick_params(axis='y', colors='#312F2F')
    # cambiar el nombre de los ejes
    ax.set_xlabel("Tipo de profundidad", fontsize=12, color='#312F2F')
    ax.set_ylabel("Magnitud", fontsize=12, color='#312F2F')
    st.pyplot(fig6)