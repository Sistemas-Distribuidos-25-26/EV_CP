from dash import html, dcc, Output, Input
import dash
import dash_bootstrap_components as dbc
from serversocket import get_state, send_state_to_central, CP_ID
import random
import time
from datetime import datetime

# Mapeo de estados a colores según la especificación
STATE_CONFIG = {
    "UNKNOWN": {"name": "Desconectado", "color": "secondary", "bg_color": "#6c757d", "text_color": "white"},
    "ACTIVE": {"name": "Activado", "color": "success", "bg_color": "#28a745", "text_color": "white"},
    "OUT_OF_ORDER": {"name": "Parado (Fuera de Servicio)", "color": "warning", "bg_color": "#fd7e14",
                     "text_color": "white"},
    "CHARGING": {"name": "Suministrando", "color": "info", "bg_color": "#007bff", "text_color": "white"},
    "BROKEN": {"name": "Averiado", "color": "danger", "bg_color": "#dc3545", "text_color": "white"},
    "DISCONNECTED": {"name": "Desconectado", "color": "secondary", "bg_color": "#6c757d", "text_color": "white"}
}

# Variables para simulación
current_consumption = 0.0
current_amount = 0.0
current_driver = None
session_start_time = None
price_per_kwh = 0.22

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


def create_status_card():
    """Crea la tarjeta de estado principal"""
    return dbc.Card([
        dbc.CardHeader([
            html.H4("Estado del Punto de Recarga", className="mb-0"),
            html.Small(f"ID: {CP_ID}", className="text-muted")
        ]),
        dbc.CardBody([
            html.Div(id="status-indicator", className="text-center mb-3"),
            html.H2(id="status-text", className="text-center mb-3"),
            html.Div(id="status-details", className="mt-3")
        ])
    ], color="light", className="mb-4")


def create_control_card():
    """Crea la tarjeta de controles"""
    return dbc.Card([
        dbc.CardHeader(html.H4("Controles del Monitor", className="mb-0")),
        dbc.CardBody([
            html.P("Simular eventos del sistema:", className="card-text"),
            dbc.ButtonGroup([
                dbc.Button("Reportar Avería", id="btn-report-failure", color="danger", className="me-2 mb-2"),
                dbc.Button("Resolver Avería", id="btn-resolve-failure", color="success", className="me-2 mb-2"),
                dbc.Button("Simular KO", id="btn-simulate-ko", color="warning", className="me-2 mb-2"),
            ], vertical=False),
            html.Hr(),
            html.P("Estado de conexión:", className="card-text"),
            html.Div(id="connection-status", children=[
                dbc.Badge("Conectado", color="success", className="me-2"),
                dbc.Badge("Engine: OK", color="success", className="me-2"),
                dbc.Badge("Central: OK", color="success")
            ])
        ])
    ], color="light", className="mb-4")


def create_telemetry_card():
    """Crea la tarjeta de telemetría (solo visible cuando está suministrando)"""
    return dbc.Card([
        dbc.CardHeader(html.H4("Telemetría en Tiempo Real", className="mb-0")),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H5("Consumo Actual", className="text-center"),
                    html.H2(id="current-consumption", children="0.0 kW", className="text-center text-primary")
                ]),
                dbc.Col([
                    html.H5("Importe Actual", className="text-center"),
                    html.H2(id="current-amount", children="0.00 €", className="text-center text-success")
                ])
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.P("Conductor:", className="mb-1"),
                    html.Strong(id="current-driver", children="Ninguno")
                ]),
                dbc.Col([
                    html.P("Tiempo de sesión:", className="mb-1"),
                    html.Strong(id="session-time", children="00:00")
                ])
            ]),
            html.Hr(),
            html.Div([
                html.H6("Historial de Estados", className="mb-2"),
                html.Div(id="state-history", style={
                    "maxHeight": "150px",
                    "overflowY": "auto",
                    "fontSize": "0.8rem"
                })
            ])
        ])
    ], color="info", id="telemetry-card", style={"display": "none"})


def create_health_monitor_card():
    """Crea la tarjeta del monitor de salud"""
    return dbc.Card([
        dbc.CardHeader(html.H4("Monitor de Salud", className="mb-0")),
        dbc.CardBody([
            dbc.Progress(id="health-progress", value=100, color="success", className="mb-3"),
            html.Div(id="health-indicators", children=[
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.I(className="bi bi-cpu me-2"),
                            "Hardware: ",
                            dbc.Badge("OK", color="success", id="hardware-status")
                        ], className="mb-2"),
                        html.Div([
                            html.I(className="bi bi-hdd me-2"),
                            "Almacenamiento: ",
                            dbc.Badge("OK", color="success", id="storage-status")
                        ], className="mb-2")
                    ]),
                    dbc.Col([
                        html.Div([
                            html.I(className="bi bi-wifi me-2"),
                            "Red: ",
                            dbc.Badge("OK", color="success", id="network-status")
                        ], className="mb-2"),
                        html.Div([
                            html.I(className="bi bi-thermometer me-2"),
                            "Temperatura: ",
                            dbc.Badge("Normal", color="success", id="temp-status")
                        ], className="mb-2")
                    ])
                ])
            ]),
            dcc.Interval(id="health-interval", interval=3000, n_intervals=0)
        ])
    ], color="light")


# Layout principal de la aplicación
app.layout = dbc.Container([
    # Header
    dbc.Navbar(
        dbc.Container([
            html.Div([
                html.I(className="bi bi-speedometer2 me-2"),
                "EV_CP_M - Monitor del Punto de Recarga",
            ], className="navbar-brand"),
            html.Div([
                dbc.Badge("Online", color="success", id="global-status", className="me-2"),
                html.Small(id="last-update", className="text-white")
            ])
        ]), color="primary", dark=True, className="mb-4"
    ),

    # Contenido principal
    dbc.Row([
        # Columna izquierda - Estado y Controles
        dbc.Col([
            create_status_card(),
            create_control_card(),
            create_health_monitor_card()
        ], width=4),

        # Columna derecha - Telemetría y Gráficos
        dbc.Col([
            create_telemetry_card(),
            dbc.Card([
                dbc.CardHeader(html.H4("Actividad del Sistema", className="mb-0")),
                dbc.CardBody([
                    html.Div(id="system-logs", style={
                        "height": "300px",
                        "overflowY": "auto",
                        "fontFamily": "monospace",
                        "fontSize": "0.8rem",
                        "backgroundColor": "#f8f9fa",
                        "padding": "10px",
                        "borderRadius": "5px"
                    })
                ])
            ])
        ], width=8)
    ]),

    # Componentes de intervalo para actualizaciones
    dcc.Interval(id="status-interval", interval=1000, n_intervals=0),
    dcc.Store(id="state-store", data=[]),  # Almacenamiento del historial de estados
    dcc.Store(id="log-store", data=[])  # Almacenamiento de logs
], fluid=True)


# Callbacks para actualizar la interfaz
@app.callback(
    [Output("status-text", "children"),
     Output("status-indicator", "children"),
     Output("status-details", "children"),
     Output("telemetry-card", "style"),
     Output("global-status", "children"),
     Output("global-status", "color")],
    [Input("status-interval", "n_intervals")]
)
def update_status(n):
    """Actualiza el estado principal del punto de recarga"""
    state = get_state()
    config = STATE_CONFIG.get(state, STATE_CONFIG["UNKNOWN"])

    # Indicador visual del estado
    indicator = html.Div(
        style={
            "width": "100px",
            "height": "100px",
            "backgroundColor": config["bg_color"],
            "borderRadius": "50%",
            "margin": "0 auto",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "color": config["text_color"],
            "fontSize": "2rem"
        },
        children=html.I(className="bi bi-lightning-charge")
    )

    # Detalles según el estado
    details = []
    global current_driver, session_start_time

    if state == "CHARGING":
        # Simular aumento del consumo
        global current_consumption, current_amount
        current_consumption = round(random.uniform(7.5, 22.0), 1)  # Entre 7.5 y 22 kW
        current_amount = round(current_amount + (current_consumption * price_per_kwh / 3600), 2)

        if not current_driver:
            current_driver = f"DRV-{random.randint(1000, 9999)}"
            session_start_time = time.time()
            add_log(f"Sesión iniciada con conductor {current_driver}")

        details = [
            html.P(f"📍 Ubicación: CP-{CP_ID}", className="mb-1"),
            html.P(f"💰 Precio: {price_per_kwh} €/kWh", className="mb-1"),
            html.P(f"👤 Conductor: {current_driver}", className="mb-1 text-primary"),
            html.P(f"⏱️ Inicio sesión: {datetime.now().strftime('%H:%M:%S')}", className="mb-1")
        ]
        telemetry_style = {"display": "block"}

    else:
        if state != "CHARGING" and current_driver:
            add_log(f"Sesión finalizada con conductor {current_driver}")
            current_driver = None
            session_start_time = None
            current_consumption = 0.0
            current_amount = 0.0

        details = [
            html.P(f"📍 Ubicación: CP-{CP_ID}", className="mb-1"),
            html.P(f"💰 Precio: {price_per_kwh} €/kWh", className="mb-1"),
            html.P("👤 Conductor: Ninguno", className="mb-1 text-muted"),
        ]
        telemetry_style = {"display": "none"}

    # Estado global
    if state in ["BROKEN", "DISCONNECTED", "UNKNOWN"]:
        global_status = "Offline"
        global_color = "danger"
    else:
        global_status = "Online"
        global_color = "success"

    return config["name"], indicator, details, telemetry_style, global_status, global_color


@app.callback(
    [Output("current-consumption", "children"),
     Output("current-amount", "children"),
     Output("current-driver", "children"),
     Output("session-time", "children")],
    [Input("status-interval", "n_intervals")]
)
def update_telemetry(n):
    """Actualiza los datos de telemetría"""
    state = get_state()

    if state == "CHARGING" and session_start_time:
        session_duration = int(time.time() - session_start_time)
        minutes = session_duration // 60
        seconds = session_duration % 60
        session_time = f"{minutes:02d}:{seconds:02d}"
    else:
        session_time = "00:00"

    return f"{current_consumption} kW", f"{current_amount} €", current_driver or "Ninguno", session_time


@app.callback(
    [Output("health-progress", "value"),
     Output("health-progress", "color"),
     Output("hardware-status", "children"),
     Output("hardware-status", "color"),
     Output("storage-status", "children"),
     Output("storage-status", "color"),
     Output("network-status", "children"),
     Output("network-status", "color"),
     Output("temp-status", "children"),
     Output("temp-status", "color")],
    [Input("health-interval", "n_intervals")]
)
def update_health_monitor(n):
    """Actualiza el monitor de salud con datos simulados"""
    state = get_state()

    if state == "BROKEN":
        health_value = random.randint(10, 30)
        health_color = "danger"
        hardware_status = ("ERROR", "danger")
        storage_status = ("ERROR", "danger")
        network_status = ("OK", "success")
        temp_status = ("ALTA", "danger")
    elif state == "DISCONNECTED":
        health_value = random.randint(40, 60)
        health_color = "warning"
        hardware_status = ("OK", "success")
        storage_status = ("OK", "success")
        network_status = ("OFFLINE", "danger")
        temp_status = ("Normal", "success")
    else:
        health_value = random.randint(85, 100)
        health_color = "success"
        hardware_status = ("OK", "success")
        storage_status = ("OK", "success")
        network_status = ("OK", "success")
        temp_status = ("Normal", "success")

    return health_value, health_color, hardware_status[0], hardware_status[1], storage_status[0], storage_status[1], \
    network_status[0], network_status[1], temp_status[0], temp_status[1]


@app.callback(
    Output("system-logs", "children"),
    [Input("status-interval", "n_intervals")]
)
def update_system_logs(n):
    """Actualiza los logs del sistema"""
    logs = get_log_store()
    if not logs:
        return html.P("No hay actividad reciente...", className="text-muted")

    log_elements = []
    for log in logs[-10:]:  # Mostrar solo los últimos 10 logs
        log_elements.append(
            html.Div([
                html.Span(log["timestamp"], className="text-muted me-2"),
                html.Span(log["message"])
            ], className="mb-1")
        )

    return log_elements


@app.callback(
    Output("last-update", "children"),
    [Input("status-interval", "n_intervals")]
)
def update_timestamp(n):
    """Actualiza la marca de tiempo"""
    return f"Última actualización: {datetime.now().strftime('%H:%M:%S')}"


# Callbacks para los controles
@app.callback(
    Output("status-interval", "n_intervals"),
    [Input("btn-report-failure", "n_clicks"),
     Input("btn-resolve-failure", "n_clicks"),
     Input("btn-simulate-ko", "n_clicks")]
)
def handle_control_actions(report_clicks, resolve_clicks, simulate_clicks):
    """Maneja las acciones de los botones de control"""
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "btn-report-failure" and report_clicks:
        send_state_to_central("BROKEN")
        add_log("⚠️ Avería reportada manualmente")

    elif button_id == "btn-resolve-failure" and resolve_clicks:
        send_state_to_central("ACTIVE")
        add_log("✅ Avería resuelta manualmente")

    elif button_id == "btn-simulate-ko" and simulate_clicks:
        add_log("❌ Simulación de KO enviada al engine")
        # Aquí se enviaría el KO al engine (simulado)

    return dash.no_update


# Funciones auxiliares para logs
log_store = []


def add_log(message):
    """Añade un mensaje al log"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_store.append({"timestamp": timestamp, "message": message})
    # Mantener solo los últimos 50 logs
    if len(log_store) > 50:
        log_store.pop(0)


def get_log_store():
    """Obtiene el almacén de logs"""
    return log_store


def run():
    """Función principal para ejecutar la GUI del monitor"""
    print(f"Interfaz del monitor disponible en: http://0.0.0.0:7000")
    add_log("Sistema de monitorización iniciado")
    add_log(f"Monitorizando punto de recarga {CP_ID}")
    app.run(host="0.0.0.0", port=7000, debug=False)
