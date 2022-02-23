#!/bin/python
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import serial
from pymongo import MongoClient
from datetime import datetime as dt
import numpy as np
import time
import pprint
import pandas as pd
import plotly
from random import random
import plotly.graph_objs as go
import re
from scipy.signal import savgol_filter

''' **************************************** '''

# TODO add constants
BAUD = 9600
IP_ADR = 27017
MINUTE_MS = 600000
PADDING = 150
BG_COLOR = '#FFFFFF'

''' MongoDB '''
client = MongoClient('localhost', IP_ADR)
db = client.beertemp
collection = db.log
entry = db.entries

''' **************************************** '''

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'padding': PADDING, 'background' : BG_COLOR}, children =[
    html.H1('Beer Temperature Logging'),
    html.H3('This is a live feed!'),
    html.Div([
        dcc.Graph(id='live-update-graph-scatter', animate=False),
        html.H3('Filter number of entries in database'),
        dcc.Input(id='resolution', value='2000', type='text'),
        dcc.Graph(id='history-graph-scatter', animate=False),
        dcc.Interval(
            id='interval-component',
            interval=1*MINUTE_MS
            )
        ])
    ])


@app.callback(Output('live-update-graph-scatter', 'figure'),
        Input('interval-component', 'n_intervals'))
def update_graph_scatter(graph_update):
    LIVE_RES = 200

    try:
        df = pd.DataFrame(list(db.entries.find().limit(int(LIVE_RES)).sort([('$natural',-1)])))
        trace = go.Scatter(
            x=df['time'],
            y=df['temperature'],
            name='Beer temperature',
            mode= 'lines+markers',
            marker = {'color': 'Blue',
                'size': 4}
            )
    except Exception as e:
        print(str(e))

    layout = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=50, b=50),
            yaxis= {'autorange': True}
            )

    fig = go.Figure(data=[trace], layout=layout)

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='Grey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='Grey')

    return fig 

# TODO callback to apply Savgol filtering
@app.callback(Output('history-graph-scatter', 'figure'),
        Input(component_id='resolution', component_property='value'))
# @app.callback(Output('live-update-graph-scatter', 'figure'))
def update_history(resolution):
    SAVGOL_WIN_LEN = 201
    # num_filter = re.compile(r'\D')
    FALLBACK_RES = 2000
    # if resolution != '' and num_filter.findall(resolution) != [] \
    if resolution != '' and int(resolution) > SAVGOL_WIN_LEN: 
        valid_res = resolution
    else:
        valid_res = FALLBACK_RES

    try:
        df = pd.DataFrame(list(db.entries.find().limit(int(valid_res)).sort([('$natural',-1)])))
        trace1 = go.Scatter(
            x=df['time'],
            y=df['temperature'],
            name='Beer temperature',
            mode= 'markers',
            marker = {'color': 'Blue',
                'size': 3}
            )

        trace2 = go.Scatter(
            x=df['time'],
            y=savgol_filter(df['temperature'], SAVGOL_WIN_LEN, 2),
            name='Filtered signal',
            mode= 'lines+markers',
            marker = {'color': 'Red',
                'size': 2}
            )
    except Exception as e:
        print(str(e))

    layout = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=50, b=50),
            yaxis= {'autorange': True}
            )

    fig = go.Figure(data=[trace1, trace2], layout=layout)

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='Grey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='Grey')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
