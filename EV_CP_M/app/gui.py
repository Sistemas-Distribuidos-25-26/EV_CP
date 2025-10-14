from dash import html, dcc, Output, Input
import dash
from engine_socket import get_state, set_state, STATES
import config
from flask import Flask
import logging

COLOR_MAP = {
    "UNKNOWN": "#b0a7b8",
    "ACTIVE": "#9de64e",
    "OUT_OF_ORDER": "#de5d3a",
    "CHARGING":"#3388de",
    "BROKEN": "#ec273f",
    "DISCONNECTED": "#b0a7b8"
}

server = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


app = dash.Dash(__name__, assets_folder="assets", server=server)

app.layout = html.Div([
    html.H1("Monitor"),
    html.H3("Monitorizando CP", id="subtitle"),
    html.Div("Estado: ", id="state-text"),
    dcc.Interval(id="interval-component", interval=1000, n_intervals=0)
], id="main-div")

@app.callback(
    [Output("state-text", "children"),
            Output("main-div", "style"),
            Output("subtitle", "children")],
    [Input("interval-component", "n_intervals")]
)
def update(n):
    style = {"backgroundColor" : COLOR_MAP.get(get_state(), "white"),
             "height": "100vh",
             "width": "100vw",
             "margin": 0, "padding" : 0,
             "display": "flex", "flexDirection": "column",
             "justifyContent": "center"}    
    return [f"Estado: {get_state()}", style, f"Monitorizando {config.CP_ID}"]

def run():
    app.run("0.0.0.0", port=7000)