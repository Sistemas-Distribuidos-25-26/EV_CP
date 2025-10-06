from dash import html, dcc, Output, Input
import dash
from serversocket import get_state

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Monitor"),
    html.H3(f"Monitorizando CP 0001", id="subtitle"),
    html.Div(f"Estado: ", id="state-text"),
    dcc.Interval(id="interval-component", interval=2000, n_intervals=0)
])

@app.callback(
    [Output("state-text", "children")],
    [Input("interval-component", "n_intervals")]
)
def update(n):
    return [f"Estado: {get_state()}"]

def run():
    app.run("0.0.0.0", port=7000)
