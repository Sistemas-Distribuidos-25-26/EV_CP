import socket
import time
from config import get_state, set_state, RECONNECTION_TIME, IP_ENGINE, PORT_ENGINE, STATES

def engine_socket():
    print(f"[EngineSocket] Conectando a {IP_ENGINE}:{PORT_ENGINE}...")
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((IP_ENGINE, PORT_ENGINE))
                print(f"[EngineSocket] Conectado a {IP_ENGINE}:{PORT_ENGINE}")

                while True:
                    try:
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