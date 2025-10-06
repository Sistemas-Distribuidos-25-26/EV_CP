import socket
import threading

STATES = [
    "UNKNOWN",
    "ACTIVE",
    "OUT_OF_ORDER",
    "CHARGING",
    "BROKEN",
    "DISCONNECTED"
]

IP = "127.0.0.1"
PORT = 5000


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
    server = socket.socket(socket.AF_INET)
    server.bind((IP, PORT))
    server.listen(5)
    print("Escuchando en el puerto " + str(PORT))

    connection, addr = server.accept()
    print("Conexión correcta!")
    try:
        while True:
            message = connection.recv(1)
            if not message:
                set_state(STATES[0])
                break

            set_state(STATES[int(message.hex())])
            print("El estado el engine es " + get_state())
    finally:
        connection.close()
        server.close()



