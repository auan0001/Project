from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import datetime

# app = Dash(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# df = pd.DataFrame({
    # "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    # "Amount": [4, 1, 2, 2, 4, 5],
    # "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

df = pd.DataFrame({
    "Broder": ["Abbe", "Janne", "Sladden", "Abbe", "Janne", "Sladden"],
    "Amount": [5, 63, 55, 2, 8, 5],
    "City": ["GBG", "KRN", "UA", "STHLM", "UA", "GBG"]
})

fig = px.bar(df, x="Broder", y="Amount", color="City", barmode="group")

def serve_layout():
    return html.H1('The time is: ' + str(datetime.datetime.now()))
app.layout = serve_layout

# app.layout = html.Div(children=[
    # html.H1('Hello TheBroder'),
    # html.H2(children='''Ablaij Statistik AB'''),
    # dcc.Graph(
        # id='Grafens graf',
        # figure=fig,
        # )
    # ])

if __name__ == '__main__':
    app.run_server(debug=True)
