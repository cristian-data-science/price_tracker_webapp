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
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.set_page_config(page_title="Prophet",layout="wide")

counter = 1

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

    



#lot2 ="https://assets8.lottiefiles.com/private_files/lf30_y7i4hgco.json"

lottie_url_h = "https://assets7.lottiefiles.com/private_files/lf30_hk1qooeo.json"
lot2= load_lottieurl(lottie_url_h)


#header_container = st.container()
#with header_container:



#st_lottie(lot2, key="hello",height=400, width=400)
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
Esta app recupera el precio y stock de las tarjetas de video de los ecommerce pcfactory y spdigital. Pronto agregaremos más tiendas!
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

col2, col3 = st.columns((4,1))

with st.sidebar:
    st_lottie(lot2, key="lol",height=300, width=300)

col1.header('Ingresa una opción')

## Sidebar - Currency price unit
#currency_price_unit = col1.selectbox('Select currency for price', ('USD', 'BTC', 'ETH'))
vendors = col1.selectbox('Selecciona la moneda', ('CLP', 'USD', 'BTC'))


#df_selected_coin = df2["modelo"]

df = pd.read_csv('resultadofinal.csv', encoding="utf'8")
df = df.drop(['Unnamed: 0'], axis=1)
df = df[['modelo','stock','precios','nombre','enlaces','tienda','precionumero']]
#df = df.sort_values("stock", ascending=False, ignore_index=True)
df = df.sort_values('stock', ascending=True, ignore_index=True)

# filtrando df con selección de tienda
sorted_coin = sorted(df["tienda"].unique())
selected_coin = col1.multiselect("Tiendas", sorted_coin, sorted_coin)
df = df[(df["tienda"].isin(selected_coin))]  # Filtering data


# filtrando df con seleción de tarjeta




df2 = pd.read_csv('top_stock.csv', encoding="utf'8")
df2['stock'] = df2['stock'].astype(int)
df2 = df2.drop(['Unnamed: 0'], axis=1)



modelselected = sorted(df["modelo"].unique())
multimodeselected = col1.multiselect("Tarjetas", modelselected, modelselected)
df = df[(df["modelo"].isin(multimodeselected))]  # Filtering data

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



minimo_select = display_data2.sort_values('precionumero').head(1)
barato_enlace = minimo_select['enlaces'].min()
barato_precio = minimo_select['precios'].min()
barato_tienda = minimo_select['tienda'].min()

if selectmodel == 'all':
    est = selectmodel
else:
    est = col2.markdown('La opción más barata para la selección esta en la tienda  '+ str(barato_tienda) +' y el precio es: ' + str(barato_precio) + ' ' + str(barato_enlace))

#col2.write(display_data2.sort_values('stock', ascending=True, ignore_index=True),width=2800, height=600)

#col2.dataframe(display_data2.sort_values('stock', ascending=True, ignore_index=True),width=2800, height=472)
#col2.dataframe(data=df, width=2800, height=600)

g2 = GridOptionsBuilder.from_dataframe(df)
g2.configure_pagination()
#gb.configure_side_bar()
g2.configure_default_column(editable=False)
gridOptions = g2.build()


with col2:
    AgGrid(display_data2, gridOptions=gridOptions,theme='streamlit',fit_columns_on_grid_load=False, enable_enterprise_modules=True, height=892)

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






loti3 = 'https://assets6.lottiefiles.com/packages/lf20_2znxgjyt.json'
lot3 =load_lottieurl(loti3)
with col3:
    st_lottie(lot3, key="loti3")#,height=74, width=200)




#col3.dataframe(data=df2, width=9800, height=1600)



col3.subheader("Top por stock")

g2 = GridOptionsBuilder.from_dataframe(df2)
#g2.configure_pagination()
#gb.configure_side_bar()
g2.configure_default_column(editable=False)
gridOptions = g2.build()

with col3:
    AgGrid(df2[['modelo','stock']], gridOptions=gridOptions,theme='streamlit',fit_columns_on_grid_load=True, enable_enterprise_modules=False,height= 600)

hide_st_style = """
            <style>

            footer {visibility: hidden;}
;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)