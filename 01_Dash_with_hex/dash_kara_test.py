#!/usr/bin/env python
# coding: utf-8

# In[4]:


import numpy as np
import pandas as pd
import plotly.express as px
import pandas as pd
import plotly.figure_factory as ff

from dash import Dash, dcc, html, Input, Output, ctx

filepath = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQQKcjObxJfMAOkArbU2-ven8yUOSYjbNiIrqPu7nbElnjE0Ad_IB3yB3I6HQnKYDx-hD34dXtxf7td/pub?gid=0&single=true&output=csv'
data = pd.read_csv(filepath)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    [
        html.Header(
            "Benthos Kara Sea",
            style={"font-size": "30px", "textAlign": "center"},
        ),
        html.Div("Biomass", style={"font-size": "20px"}),
        "g/m2  ",
        dcc.Input(id="meter", value=10, type="number", step=1),
        
        html.Div("Depth", style={"font-size": "20px"}),
        "g/m2  ",
        dcc.Input(id="shan", value= 0, type="number", step=1),
        
        html.Div("Cell", style={"font-size": "20px"}),
       "hex size",
        dcc.Input(id="cell", value= 6, type="number", step=1),
        
        dcc.Graph(id="map"),
    ],
    style={"margin": 10, "maxWidth": 800},
)


@app.callback(
    Output("meter", "value"),
    Output("shan", "value"),
    Output("cell", "value"),
    Output("map", "figure"),
    Input("meter", "value"),
    Input("shan", "value"),
    Input("cell", "value")
)
def sync_input(meter, shan, cell):
    if cell < 2:
        cell = 2
        print('you have to set hex cell not less than 2')
    if meter > 142:
        meter = 142
        print('you have to biomass not more than 142')
    if shan < -34:
        shan = -34
        print('you have to set hex cell not less than -34')  
        
        
    fig = ff.create_hexbin_mapbox(
        data_frame=data.query('total_biomass >= @meter and depth < @shan'), lat="lat", lon="lon", 
        nx_hexagon=cell, opacity=0.7, labels={"color": 'shanone'},
        color="shanone", agg_func=np.mean, color_continuous_scale="plotly3", range_color=[0,4], mapbox_style = 'open-street-map',
        show_original_data=True, original_data_marker=dict(size=4, opacity=0.6, color="deeppink"))

    fig.update_layout(margin=dict(b=66, t=73, l=70, r=75))
    fig.show()
      
    return meter, shan, cell, fig


if __name__ == "__main__":
    app.run_server(debug=True)


# In[ ]:




