import socket
import threading
import time

STATES = [
    "UNKNOWN",
    "ACTIVE",
    "OUT_OF_ORDER",
    "CHARGING",
    "BROKEN",
    "DISCONNECTED"
]

IP_Engine = "127.0.0.1"
PORT_Engine = 5000
IP_Central = "127.0.0.1"
PORT_Central = 5000
CP_ID = "0001"

RECONNECTION_TIME = 2

_STATE = STATES[0]
_LOCK = threading.Lock()

def set_state(state: str):
    global _STATE
    with _LOCK:
        _STATE = state

def get_state() -> str:
    with _LOCK:
        return _STATE

def run_socket():

    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((IP_Engine, PORT_Engine))
                print(f"[EngineSocket] Conectado a {IP_Engine}:{PORT_Engine}")

                while True:
                    try:
                        print("[EngineSocket] Mandando request de estado...")
                        s.send(bytes([1]))
                        state = s.recv(1)
                        if not state:
                            set_state(STATES[0])
                        else:
                            set_state(STATES[int(state.hex())])
                        print("[EngineSocket] El estado el engine es " + get_state())
                        time.sleep(1)
                    except s.timeout:
                        set_state(STATES[0])
                        print("[EngineSocket]  El estado el engine es " + get_state())
        except Exception as e:
            print(f"[EngineSocket] Se ha perdido la señal con el servidor, reintentando en {RECONNECTION_TIME} segundos...")
            time.sleep(RECONNECTION_TIME)