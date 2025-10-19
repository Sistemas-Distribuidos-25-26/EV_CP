import threading

STATES = [
    "UNKNOWN",
    "ACTIVE",
    "OUT_OF_ORDER",
    "CHARGING",
    "BROKEN",
    "DISCONNECTED"
]


RECONNECTION_TIME = 2

OLD_STATE = STATES[0]
_STATE = STATES[3]
_LOCK = threading.Lock()


IP_ENGINE = "127.0.0.1"
PORT_ENGINE = 5000
IP_CENTRAL = "127.0.0.1"
PORT_CENTRAL = 6000

CP_ID = "CP001"


def set_state(state: str):
    global _STATE
    with _LOCK:
        OLD_STATE = _STATE
        _STATE = state

def get_state() -> str:
    with _LOCK:
        return _STATE