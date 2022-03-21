#!/bin/python
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import serial
from pymongo import MongoClient
from datetime import datetime as dt
from datetime import date
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
HOUR_MS = 60*600000
PADDING = 150
BG_COLOR = '#FFFFFF'

''' MongoDB '''
client = MongoClient('localhost', IP_ADR)
db = client.beertemp
settings = db.settings
entry = db.entries

''' **************************************** '''

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'padding': PADDING, 'background' : BG_COLOR}, children =[
    html.H1('Beer Temperature Logging'),
    html.H3('This is a live feed!'),
    html.Div([
        dcc.Graph(id='live-update-graph-scatter', animate=False),
        html.Hr(),
        dcc.Interval(
            id='interval-component',
            interval=1*HOUR_MS
            )
        ]),
    html.Div([
        html.H3('Set temperature alarm value'),
        # dcc.Input(
            # id="input_range_min", type="number", debounce=True, placeholder="Set min temp",
            # min=-5, max=40, step=1, value=int(settings.find_one({"_id": "settings"})['min'])
            # ),
        # dcc.Input(
            # id="input_range_max", type="number", debounce=True, placeholder="Set max temp",
            # min=-5, max=40, step=1, value=int(settings.find_one({"_id": "settings"})['max'])
            # ),
        dcc.Input(
            id="input_range_drop", type="number", debounce=True, placeholder="Temp drop tolerance",
            min=1, max=40, step=1, value=int(settings.find_one({"_id": "settings"})['drop'])
            ),
        # html.Div(id="min-max-out"),
        html.Div(id="drop-out"),
        html.H3('Set start and end date'),
        dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed = entry.find_one()['time'].date(),
            max_date_allowed = list(entry.find().sort('$natural',-1).limit(1))[0]['time'].date(),

            # TODO timedelta based fallback
            start_date = date(2022,2,28),
            end_date = date(2022,3,4)
            ),
        dcc.Graph(id='history-graph-scatter', animate=False),
        html.Div(id='output-container-date-picker-range')
        ]),
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
        [Input(component_id='date-picker-range', component_property='start_date'),
        Input(component_id='date-picker-range',component_property='end_date')]
        )
# @app.callback(Output('live-update-graph-scatter', 'figure'))
def update_history(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df = pd.DataFrame(list(db.entries.find().sort([('_id',-1)])))

    filtered_df = df[df['time'].between(
        dt.strftime(start_date, "%Y-%m-%d"),
        dt.strftime(end_date, "%Y-%m-%d")
    )]

    SAVGOL_WIN_LEN = 201

    try:
        # trace1 = go.Scatter(
            # x=df['time'],
            # y=df['temperature'],
            # name='Beer temperature',
            # mode= 'markers',
            # marker = {'color': 'Blue',
                # 'size': 3}
            # )

        trace2 = go.Scatter(
            x=filtered_df['time'],
            # y=savgol_filter(filtered_df['temperature'], SAVGOL_WIN_LEN, 2),
            y=filtered_df['temperature'],
            name='Sensor signal [C]',
            # name='Filtered signal',
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

    # fig = go.Figure(data=[trace1, trace2], layout=layout)
    fig = go.Figure(data=trace2, layout=layout)
    min_temp = filtered_df['temperature'].min() 
    max_temp = filtered_df['temperature'].max() 
    mean_temp = filtered_df['temperature'].mean() 

    fig.add_annotation(text="Min = " + str(min_temp) + " C",
        xref="paper", yref="paper",
        x=0.1, y=1, showarrow=False, 
           font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
            ),
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="red",
        opacity=0.8
        )

    fig.add_annotation(text="Max = " + str(max_temp) + " C",
        xref="paper", yref="paper",
        x=0.9, y=1, showarrow=False, 
           font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
            ),
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="red",
        opacity=0.8
        )

    fig.add_annotation(text="Mean = " + str(round(mean_temp, 3)) + " C",
        xref="paper", yref="paper",
        x=0.5, y=1, showarrow=False, 
           font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
            ),
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="red",
        opacity=0.8
        )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='Grey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='Grey')

    return fig

# @app.callback(
    # Output("min-max-out", "children"),
    # Input("input_range_min", "value"),
    # Input("input_range_max", "value"),
# )
# def set_temp_min_max(rangemin, rangemax):
    # # if rangemin or rangemax == None:
        # # return "Temperature(s) out of range"
    # if rangemin >= rangemax:
        # return "Min has to be lower than max"
    # else:
        # settings.update_one({"_id": "settings"}, {"$set":{"min": rangemin, "max": rangemax}})
        # return "Max temp: {}C | Min temp: {}C".format(rangemin, rangemax)

@app.callback(
    Output("drop-out", "children"),
    Input("input_range_drop", "value"),
)
def set_temp_drop(rangedrop):
    if rangedrop == None:
        return "Temp drop out of range"
    else:
        settings.update_one({"_id": "settings"}, {"$set":{"drop": rangedrop}})
        return "Warning if temperature drops >= {} C".format(rangedrop)

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
