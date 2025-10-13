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

#Variables de configuración (deben venir de los argumentos)
IP_Engine = "127.0.0.1"
PORT_Engine = 5000
IP_Central = "127.0.0.1"
PORT_Central = 5000
CP_ID = "0001" #Por defecto, se puede sobreescribir

_STATE = STATES[0]
_LOCK = threading.Lock()

def set_state(state: str):
    global _STATE
    with _LOCK:
        old_state = _STATE
        _STATE = state
        print(f"Estado cambio: {old_state} -> {state}")
        if old_state != state:
            send_state_to_central(state)

def get_state() -> str:
    """Obtiene el estado actual del punto de recarga"""
    with _LOCK:
        return _STATE

def send_state_to_central(state: str):
    """Envía el estado actual a la central"""
    try:
        """Formatear mensaje según protocolo"""
        state_mapping = {
            "ACTIVE": "Activado",
            "OUT_OF_ORDER": "Parado",
            "CHARGING": "Suministrando",
            "BROKEN": "Averiado",
            "DISCONNECTED": "Desconectado",
            "UNKNOWN": "Desconectado"
        }

        estado_central = state_mapping.get(state, "Desconectado")
        mensaje = f"Estado actualizado#{CP_ID}#{estado_central}"

        lrc = 0
        for char in mensaje:
            lrc ^= ord(char)
        lrc_char = chr(lrc % 256)

        mensaje_formateado = f"<STX>{mensaje}#{lrc_char}<ETX>"

        """Enviar a la central via socket"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((IP_Central, PORT_Central))
            sock.send(mensaje_formateado.encode('utf-8'))
            respuesta = sock.recv(1024).decode('utf-8')
            print(f"Central respondió: {respuesta}")

    except Exception as e:
        print(f"Error enviado estado a central: {e}")

def handle_engine_connection(connection, addr):
    """Maneja la conexión con el engine"""
    print(f"Conexión estableciada con Engine en {addr}")
    try:
        while True:
            message = connection.recv(1)
            if not message:
                set_state(STATES[0])
                break
            try:
                state_index = int(message.hex())
                if 0 <= state_index < len(STATES):
                    set_state(STATES[state_index])
                    print(f"Estado del engine actualizado:{STATES[state_index]}")
                else:
                    print(f"Índice de estado inválido: {state_index}")
            except ValueError:
                print(f"Mensaje inválido recibido: {message}")
    except ConnectionResetError:
        print("Conexión con Engine resetada")
    except Exception as e:
        print(f"Error en la conexión con Engine: {e}")
    finally:
        connection.close()



def run_socket():
    """Ejecuta el servidor socket para comunicación con el Engine"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((IP_Engine, PORT_Engine))
    server.listen(5)
    print("Escuchando en el puerto " + str(PORT_Engine))

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



