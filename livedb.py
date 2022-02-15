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
    line = ser.readline().decode()
    if len(line) > 6:   # if not trash
        temp = (float(line.strip('\x00\n')))
    else:               # try again
        line = ser.readline().decode()
        temp = (float(line.strip('\x00\n')))
    return temp

def temp_to_db(temp):
    temp_entry = {"temperature": get_temperature(temp),
            "time": dt.utcnow()} 
    posts.insert_one(temp_entry)

def main():
   posts.drop()
   while True:
       temp_to_db(temp)
       time.sleep(1)
       df = pd.DataFrame(list(db.posts.find()))
       print(df)

''' **************************************** '''
app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div([
        dcc.Graph(id='live-update-graph-scatter', animate=True),
        dcc.Graph(id='live-update-graph-bar'),
        dcc.Interval(
            id='interval-component',
            interval=1*2000
        )
    ])
)


# State?
@app.callback(Output('live-update-graph-scatter', 'figure'),
              [Input('interval-component', 'n_intervals')])
# @app.callback(Output('live-update-graph-scatter', 'figure'))
def update_graph_scatter(graph_update):
    traces = list()
    temp_to_db(temp)
    df = pd.DataFrame(list(db.posts.find()))
    traces.append(plotly.graph_objs.Scatter(
        x=df['time'],
        y=df['temperature'],
        name='Beer temperature',
        mode= 'lines+markers'
        ))
    return {'data': traces}

# State?
@app.callback(Output('live-update-graph-bar', 'figure'),
              [Input('interval-component', 'n_intervals')])
# @app.callback(Output('live-update-graph-bar', 'figure'))
def update_graph_bar(graph_update):

    traces = list()
    for t in range(2):
        traces.append(plotly.graph_objs.Bar(
            x=[1, 2, 3, 4, 5],
            y=[(t + 1) * random() for i in range(5)],
            name='Bar {}'.format(t)
            ))
    layout = plotly.graph_objs.Layout(
    barmode='group'
)
    return {'data': traces, 'layout': layout}


if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")

# if __name__ == '__main__':
    # main()
