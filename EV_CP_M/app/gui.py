import os

from dash import html, dcc, Output, Input
import dash
import config
from flask import Flask
import logging

COLOR_MAP = {
    "DESCONECTADO": "#b0a7b8",
    "ACTIVO": "#9de64e",
    "FUERA DE SERVICIO": "#de5d3a",
    "SUMINISTRANDO":"#3388de",
    "K.O.": "#ec273f",
    "AVERIADO": "#ec273f"
}

server = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


app = dash.Dash(__name__, assets_folder="assets", server=server)

app.layout = html.Div([
    html.H1("Monitor"),
    html.H3("Monitorizando CP", id="subtitle"),
    html.Div("Estado: ", id="state-text"),
    html.Div([
        html.P("", id="pairing_label"),
        html.Button("Conectar", id="charge_button", n_clicks=0),
        html.Button("Parar", id="stop_button", n_clicks=0)
    ],id="charge-div"),
    html.Div([
        html.P("Total suministrado: 0kWh",id="charging_status"),
        html.P("Suministro restante: 0kWh", id="remaining_status")
    ], id="charging_info", hidden=False),
    dcc.Interval(id="interval-component", interval=1000, n_intervals=0)
], id="main-div")

@app.callback(
    Output("charging_info", "hidden"),
    Input("charge_button", "n_clicks")
)
def start_charging(n):
    if config.get_state() == "ACTIVO":
        config.IS_CHARGING = True
    return False

@app.callback(
    Output("main-div","hidden"),
    Input("stop_button", "n_clicks")
)
def stop_charging(n):
    config.IS_CHARGING = False
    return False


@app.callback(
    [Output("state-text", "children"),
            Output("main-div", "style"),
            Output("subtitle", "children"),
            Output("pairing_label", "children"),
            Output("remaining_status", "children"),
            Output("charging_status", "children")],
    [Input("interval-component", "n_intervals")]
)
def update(n):
    style = {"backgroundColor" : COLOR_MAP.get(config.get_state(), "white"),
             "height": "100vh",
             "width": "100vw",
             "margin": 0, "padding" : 0,
             "display": "flex", "flexDirection": "column",
             "justifyContent": "center"}
    if n % 2 == 0 and config.IS_CHARGING and (config.get_state() != "SUMINISTRANDO" or config.REMAINING_POWER <= 0):
        config.IS_CHARGING = False
    return [f"Estado: {config.get_state()}",
            style,
            f"Monitorizando {config.CP_ID}",
            f"Vinculado a {config.PAIRED}" if config.PAIRED else "",
            f"Suministro restante: {config.REMAINING_POWER:.3f}kWh",
            f"Total suministrado: {config.TOTAL_CHARGED:.3f}kWh"]

def run():
    app.run("0.0.0.0", port=int(os.getenv("PORT", 7000)))