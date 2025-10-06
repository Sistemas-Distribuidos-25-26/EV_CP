from sys import argv
from serversocket import run_socket
import threading
from gui import run

socket_thread = threading.Thread(target=run_socket)
socket_thread.daemon = True
socket_thread.start()

if len(argv) < 3:
    print("Uso: EV_CP_M [IP_Engine] [Puerto_Engine]")
    exit(-1)

IP = argv[1]
PORT = int(argv[2])

run()