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

''' **************************************** '''
ser = serial.Serial("/dev/ttyUSB0", 9600)

temp = 0

''' MongoDB '''
client = MongoClient('localhost', 27017)
db = client.test_db
collection = db.btlog
posts = db.posts
posts.drop()

def get_temperature(temp):
    ser.write(bytes(b'R'))
    line = ser.readline().decode()
    if len(line) > 6 and float(line.strip('\x00\n')) < 50:   # if not trash
        temp = (float(line.strip('\x00\n')))
    # else:               # try again
        # line = ser.readline().decode()
        # temp = (float(line.strip('\x00\n')))
    return temp

def temp_to_db(temp):
    temp_entry = {"temperature": get_temperature(temp),
            "time": dt.utcnow()} 
    posts.insert_one(temp_entry)

''' **************************************** '''

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('Beer Temperature Logging'),
    html.H3('This is a live feed!'),
    html.Div([
        dcc.Graph(id='live-update-graph-scatter', animate=False),
        html.H3('Filter number of entries in database'),
        dcc.Input(id='resolution', value='20', type='text'),
        dcc.Graph(id='history-graph-scatter', animate=False),
        dcc.Interval(
            id='interval-component',
            interval=1*2000
            )
        ])
    ])


@app.callback(Output('live-update-graph-scatter', 'figure'),
        Input('interval-component', 'n_intervals'))
def update_graph_scatter(graph_update):
    traces = list()
    temp_to_db(temp)
    live_res = 20
    temp_offset = 2

    df = pd.DataFrame(list(db.posts.find().limit(int(live_res)).sort([('$natural',-1)])))
    traces.append(plotly.graph_objs.Scatter(
    x=df['time'],
    y=df['temperature'],
    name='Beer temperature',
    mode= 'lines+markers'
    ))

    layout = plotly.graph_objs.Layout(
            yaxis=dict(range=[min(df['temperature'])-temp_offset,
                max(df['temperature'])+temp_offset]))
    return {'data': traces, 'layout': layout}

# State?
@app.callback(Output('history-graph-scatter', 'figure'),
        Input(component_id='resolution', component_property='value'))
# @app.callback(Output('live-update-graph-scatter', 'figure'))
def update_history(resolution):
    # num_filter = re.compile(r'\D')
    traces = list()
    fallback_res = 200
    # if resolution != '' and num_filter.findall(resolution) != [] \
    if resolution != '' and int(resolution) > 0: 
        valid_res = resolution
    else:
        valid_res = fallback_res

    df = pd.DataFrame(list(db.posts.find().limit(int(valid_res)).sort([('$natural',-1)])))
    traces.append(plotly.graph_objs.Scatter(
    x=df['time'],
    y=df['temperature'],
    name='Beer temperature',
    mode= 'lines+markers'
    ))

    layout = plotly.graph_objs.Layout(
            yaxis=dict(range=[min(df['temperature'])-2,
                max(df['temperature'])+2]))
    return {'data': traces, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
