import time
from tkinter.tix import COLUMN
import streamlit as st
import numpy as np
import pandas as pd

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = pd.DataFrame(
     np.random.rand(1, 3),
     columns=['PcFactory', 'SPDigital', 'Winpy'])

chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows + np.random.rand(1, 3).cumsum(axis=0)
    status_text.text("%i%% Completado" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows +0.4
    time.sleep(0.02)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")


xx=pd.DataFrame(
     np.random.randn(1, 3),
     columns=['PcFactory', 'SPDigital', 'Winpy'])

xx