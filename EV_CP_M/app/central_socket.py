import socket
import time
import config

STX = b'\x02'
ETX = b'\x03'
EOT = b'\x04'
ENQ = b'\x05'
ACK = b'\x06'
NACK = b'\x15'

logged = False

def get_payload():
    if not logged:
        return f"A#{config.CP_ID}#{config.get_state()}" # Mandar más info (nombre, coordenadas, precio...)
    else:
        return f"S#{config.CP_ID}#{config.get_state()}"

def calculate_lrc(data):
    lrc = 0
    for byte in data:
        lrc ^= byte
    return bytes([lrc])

def central_socket():
    global logged
    while True:
        print(f"[CentralSocket] Conectando a {config.IP_CENTRAL}:{config.PORT_CENTRAL}...")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((config.IP_CENTRAL, config.PORT_CENTRAL))
                print(f"[CentralSocket] Conectado a {config.IP_CENTRAL}:{config.PORT_CENTRAL}")

                while True:
                    print("[CentralSocket] Notificando a la central...")

                    s.send(ENQ)
                    response = s.recv(1)
                    if response == NACK:
                        print(f"[CentralSocket] No se puede establecer conexión con la central, reintentando en {config.RECONNECTION_TIME} segundos...")
                        time.sleep(config.RECONNECTION_TIME)
                        continue

                    while True:
                        payload = get_payload().encode()
                        message = STX + payload + ETX + calculate_lrc(payload)
                        s.send(message)
                        response = s.recv(1)
                        if response == NACK:
                            print( f"[CentralSocket] La central no ha recibido el estado correctamente")
                            s.send(EOT)
                            break
                        if response == ACK and not logged:
                            logged = True
                        time.sleep(1)
        except:
            print(f"[CentralSocket] Se ha perdido la señal con la central, reintentando en {config.RECONNECTION_TIME} segundos...")
            time.sleep(config.RECONNECTION_TIME)

        s.close()