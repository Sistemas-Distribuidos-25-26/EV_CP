import socket
import time
from config import get_state, RECONNECTION_TIME, IP_CENTRAL, PORT_CENTRAL, CP_ID

def central_socket():

    while True:
        print(f"[CentralSocket] Conectando a {IP_CENTRAL}:{PORT_CENTRAL}...")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((IP_CENTRAL, PORT_CENTRAL))
                print(f"[CentralSocket] Conectado a {IP_CENTRAL}:{PORT_CENTRAL}")

                while True:
                    print("[CentralSocket] Notificando a la central...")
                    message = CP_ID + "," + get_state()
                    s.send(message.encode())
                    time.sleep(1)
        except:
            print(f"[CentralSocket] Se ha perdido la señal con la central, reintentando en {RECONNECTION_TIME} segundos...")
            time.sleep(RECONNECTION_TIME)