import threading

STATES = [
    "DESCONECTADO",
    "ACTIVO",
    "FUERA DE SERVICIO",
    "SUMINISTRANDO",
    "K.O.",
    "AVERIADO"
]

RECONNECTION_TIME = 2

_STATE = STATES[0]
_LOCK = threading.Lock()

IS_CHARGING = False
IP_ENGINE = "127.0.0.1"
PORT_ENGINE = 5000
IP_CENTRAL = "127.0.0.1"
PORT_CENTRAL = 6000

CP_ID = "CP001"

PRICE = 0.34

PAIRED = ""

TOTAL_CHARGED = 0
REMAINING_POWER = 0

def set_state(state: str):
    global _STATE
    with _LOCK:
        _STATE = state

def get_state() -> str:
    with _LOCK:
        return _STATE