from sys import argv
from engine_socket import engine_socket
from central_socket import central_socket
import threading
import config
from gui import run

if len(argv) < 6:
    print("Uso: EV_CP_M [IP_Engine] [Puerto_Engine] [IP_Central] [Puerto_Central] [Identificador]")
    exit(-1)

config.IP_ENGINE = argv[1]
config.PORT_ENGINE = int(argv[2])
config.IP_CENTRAL = argv[3]
config.PORT_CENTRAL = int(argv[4])
config.CP_ID = argv[5]


socket_thread = threading.Thread(target=engine_socket, daemon=True)
socket_thread.start()

socket_thread = threading.Thread(target=central_socket, daemon=True)
socket_thread.start()

run()
