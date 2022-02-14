import encodings
from operator import index
import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import time
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner


#---------------------------------#
# New feature (make sure to upgrade your streamlit library)
# pip install --upgrade streamlit

#---------------------------------#
# Page layout
## Page expands to full width
#st.set_page_config(layout="wide")
#---------------------------------#
# Title

#image = Image.open('./images/ptgblue.png')

#st.image(image, width = 650)

st.title('Rastreador de tarjetas de video en Chile')
st.markdown("""
Esta app hace un siguimiento de los precios de las tarjetas de video de los ecommerce de pcfactory y spdigital. Pronto agregaremos más vendedores!
""")

#---------------------------------#
# About
expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** base64, pandas, streamlit, numpy, BeautifulSoup, requests, json, time
* **Data source:** Web scraping [pcfactory](https://www.pcfactory.cl/) & [spdigital](https://www.spdigital.cl/).
* **Credit:** Web scraper adaptado del articulo de deepnote *[Web Scraping y analisis de datos](https://deepnote.com/@cristian-gutierrez/Web-Scraping-y-analisis-de-datos-WYrIuoDkRKOx6kN4kG9VQA).
""")


#---------------------------------#
# Page layout (continued)
## Divide page to 3 columns (col1 = sidebar, col2 and col3 = page contents)
col1 = st.sidebar
col2, col3 = st.columns((4,1))

col1.header('Ingresa una opción')

## Sidebar - Currency price unit
#currency_price_unit = col1.selectbox('Select currency for price', ('USD', 'BTC', 'ETH'))
vendors = col1.selectbox('Selecciona la moneda', ('CLP', 'USD', 'BTC'))

df = pd.read_csv('resultadofinal.csv', encoding="utf'8")
df = df.drop(['Unnamed: 0'], axis=1)
df = df.sort_values("stock", ascending=True)
#df = df.set_index('nombre')
#df.index.name="modelo de tarjeta"


col2.subheader("Precios de tarjetas gráficas")

#col2.dataframe(df)
#col2.dataframe(df)
st.dataframe(data=df, width=1800, height=400)


df2 = df
from IPython.display import HTML
HTML(df2.to_html(render_links=True, escape=False))










# Download CSV data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=True, encoding = "utf'8")
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="video_cards.csv">Descargar data en csv</a>'
    return href

st.markdown(filedownload(df), unsafe_allow_html=True)