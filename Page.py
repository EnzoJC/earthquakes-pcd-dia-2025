import streamlit as st
import pandas as pd
import numpy as np

# Define the pages
main_page = st.Page("Home.py", title="Home", icon="🏠")
page_1 = st.Page("Main.py", title="Datos", icon="📉")

# Set up navigation
pg = st.navigation([main_page, page_1])

# Run the selected page
pg.run()