from dash import html, dcc, Output, Input
import dash
from engine_socket import get_state, set_state, STATES

COLOR_MAP = {
    "UNKNOWN": "#b0a7b8",
    "ACTIVE": "#9de64e",
    "OUT_OF_ORDER": "#de5d3a",
    "CHARGING":"#3388de",
    "BROKEN": "#ec273f",
    "DISCONNECTED": "#b0a7b8"
}


app = dash.Dash(__name__, assets_folder="assets")

app.layout = html.Div([
    html.H1("Monitor"),
    html.H3(f"Monitorizando CP 0001", id="subtitle"),
    html.Div(f"Estado: ", id="state-text"),
    dcc.Interval(id="interval-component", interval=2000, n_intervals=0)
], id="main-div")

@app.callback(
    [Output("state-text", "children"),
            Output("main-div", "style")],
    [Input("interval-component", "n_intervals")]
)
def update(n):
    state = get_state()
    style = {"backgroundColor" : COLOR_MAP.get(state, "white"),
             "height": "100vh",
             "width": "100vw",
             "margin": 0, "padding" : 0,
             "display": "flex", "flexDirection": "column",
             "justifyContent": "center"}
    return [f"Estado: {state}", style]

def run():
    app.run("0.0.0.0", port=7000)