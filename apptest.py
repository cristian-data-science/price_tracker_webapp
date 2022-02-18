import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models import DataTable, TableColumn, HTMLTemplateFormatter
from streamlit_bokeh_events import streamlit_bokeh_events

df2 = pd.read_csv("resultadofinal.csv")
df2['links'] = df2['enlaces']
df3 = df2
df3 = pd.DataFrame(df3)

# create plot
cds = ColumnDataSource(df3)
columns = [
TableColumn(field="links", title="links", formatter=HTMLTemplateFormatter(template='<a href="<%= value %>"target="_blank"><%= value %>')),
]

pd.DataFrame(columns)


# define events

p = DataTable(source=cds, columns=columns, css_classes=["my_table"])
result = streamlit_bokeh_events(bokeh_plot=p, events="INDEX_SELECT", key="foo", refresh_on_update=False, debounce_time=0, override_height=100)


pd.DataFrame(columns)
columns