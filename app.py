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
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.set_page_config(page_title="Prophet",layout="wide")

counter = 1

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

    

lottie_url_hello = "https://assets7.lottiefiles.com/packages/lf20_49rdyysj.json"
lottie_url_download = "https://assets4.lottiefiles.com/private_files/lf30_t26law.json"
lottie_hello = load_lottieurl(lottie_url_hello)
lottie_download = load_lottieurl(lottie_url_download)
lot2 ="https://assets8.lottiefiles.com/private_files/lf30_y7i4hgco.json"

lottie_url_h = "https://assets7.lottiefiles.com/private_files/lf30_hk1qooeo.json"
lottie_url_download = "https://assets4.lottiefiles.com/private_files/lf30_t26law.json"
lot2= load_lottieurl(lottie_url_h)
lottie_download = load_lottieurl(lottie_url_download)


#header_container = st.container()
#with header_container:



#st_lottie(lottie_hello, key="hello",height=400, width=400)
st.title('Price & Stock Tracker')


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

#st.title('Rastreador de tarjetas de video en Chile')
st.markdown("""
Esta app recupera el precio y stock de las tarjetas de video de los ecommerce pcfactory y spdigital. Pronto agregaremos más vendedores!
""")

#---------------------------------#
# About
expander_bar = st.expander("About")
expander_bar.markdown("""
*   Esta app consume datos de un webscaper automatizado y muestra la data de forma ordenada. En un update futuro se conectará con un bot de telegram para notificar variaciones de precios o alertas personalizadas
* **Librerías de python utilizadas:** base64, pandas, streamlit, numpy, requests, json, time
* **Data source:** Web scraping [pcfactory](https://www.pcfactory.cl/) & [spdigital](https://www.spdigital.cl/) (pronto agregaremos más)
* **Credit:** Web scraper adaptado del articulo de deepnote [Web Scraping y analisis de datos](https://deepnote.com/@cristian-gutierrez/Web-Scraping-y-analisis-de-datos-WYrIuoDkRKOx6kN4kG9VQA).
""")


#---------------------------------#
# Page layout (continued)
## Divide page to 3 columns (col1 = sidebar, col2 and col3 = page contents)
col1 = st.sidebar

col2, col3 = st.columns((2,1))

with st.sidebar:
    st_lottie(lot2, key="lol")#,height=400, width=400)

col1.header('Ingresa una opción')

## Sidebar - Currency price unit
#currency_price_unit = col1.selectbox('Select currency for price', ('USD', 'BTC', 'ETH'))
vendors = col1.selectbox('Selecciona la moneda', ('CLP', 'USD', 'BTC'))

df2 = pd.read_csv('top_stock.csv', encoding="utf'8")
df2['stock'] = df2['stock'].astype(int)




#df_selected_coin = df2["modelo"]

df = pd.read_csv('resultadofinal.csv', encoding="utf'8")
df = df.drop(['Unnamed: 0'], axis=1)
df = df.sort_values("stock", ascending=False, ignore_index=True)


sorted_coin = sorted(df["tienda"].unique())
selected_coin = col1.multiselect("Tiendas", sorted_coin, sorted_coin)

modelselected = sorted(df2["modelo"])
multimodeselected = col1.multiselect("Tarjetas", modelselected, modelselected)

#df = df.set_index('nombre')
#df.index.name="modelo de tarjeta"



#pd.set_option('display.max_colwidth', -1)

#col2.subheader("Precios de tarjetas gráficas")

#col2.dataframe(df)
#col2.dataframe(df)






model_list = ['All'] + df['modelo'].unique().tolist()
#model_list = sorted(model_list)



selectmodel = col2.selectbox('Selecciona un modelo:',model_list, key='modelo')
# display the collected input
# st.write('Tu selección actual: ' + str(selectmodel))

if selectmodel != 'All':
	display_data2 = df[df['modelo'] == selectmodel]
else:
	display_data2 = df.copy()

#col2.write(display_data2.sort_values('stock', ascending=True, ignore_index=True),width=2800, height=600)


gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination()
gb.configure_side_bar()
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=False)
gridOptions = gb.build()



col2.dataframe(data=display_data2.sort_values('stock', ascending=True, ignore_index=True),width=2800, height=472)
#col2.dataframe(data=df, width=2800, height=600)


AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True)







# Download CSV data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
#def filedownload(df):
#    csv = df.to_csv(index=True, encoding = "utf'8")
#    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
#    href = f'<a href="data:file/csv;base64,{b64}" download="video_cards.csv">Descargar data en csv</a>'
#    return href
#
#st.markdown(filedownload(df), unsafe_allow_html=True)

#st.markdown(filedownload(df.to_excel('prueba.xlsx')), unsafe_allow_html=True)

from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data
df_xlsx = to_excel(df)
col2.download_button(label='📥 Descargar a Excel',
                                data=df_xlsx ,
                                file_name= 'data_video_cards.xlsx')


col3.subheader("Top por stock")

df2 = df2.drop(['Unnamed: 0'], axis=1)
col3.dataframe(data=df2, width=9800, height=1600)

hide_st_style = """
            <style>

            footer {visibility: hidden;}
;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)