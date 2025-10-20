import socket
import time
import config

def engine_socket():
    print(f"[EngineSocket] Conectando a {config.IP_ENGINE}:{config.PORT_ENGINE}...")
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((config.IP_ENGINE, config.PORT_ENGINE))
                print(f"[EngineSocket] Conectado a {config.IP_ENGINE}:{config.PORT_ENGINE}")

                while True:
                    try:
                        s.send(b'\x01' if config.IS_CHARGING else b'\x00')

                        state = s.recv(1)
                        message = s.recv(64).decode()
                        data = message.split("#")
                        paired = data[0]
                        if not state:
                            config.set_state(config.STATES[5])
                        else:
                            config.set_state(config.STATES[int(state.hex())])
                        config.PAIRED = paired
                        print("[EngineSocket] El estado el engine es " + config.get_state())
                        if paired:
                            print(f"[EngineSocket] Emparejado a: {paired}")

                        status = data[1]
                        config.REMAINING_POWER = float(status)
                        charged = data[2]
                        config.TOTAL_CHARGED = float(charged)

                        time.sleep(1)
                    except s.timeout:
                        config.set_state(config.STATES[0])
                        print("[EngineSocket]  El estado el engine es " + config.get_state())
        except:
            print(f"[EngineSocket] Se ha perdido la señal con el servidor, reintentando en {config.RECONNECTION_TIME} segundos...")
            time.sleep(config.RECONNECTION_TIME)