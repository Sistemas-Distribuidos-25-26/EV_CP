from sys import argv
from serversocket import run_socket
import threading
from gui import run

socket_thread = threading.Thread(target=run_socket)
socket_thread.daemon = True
socket_thread.start()

if len(argv) < 5:
    print("Uso: EV_CP_M [IP_Engine] [Puerto_Engine] [IP_Central] [Puerto_Central]")
    exit(-1)

IP_Engine = argv[1]
PORT_Engine = int(argv[2])
IP_Central = argv[3]
PORT_Central = int(argv[4])
CP_ID = "CP001"

print(f"Configuración Monitor:")
print(f"  - Engine: {IP_Engine}:{PORT_Engine}")
print(f"  - Central: {IP_Central}:{PORT_Central}")
print(f"  - CP ID: {CP_ID}")

run()
