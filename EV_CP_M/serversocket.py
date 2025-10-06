import socket
from sys import argv

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
                break
            print("El estado el engine es " + STATES[int(message.hex())])
    finally:
        connection.close()
        server.close()

if len(argv) < 3:
    print("Uso: EV_CP_M [IP_Engine] [Puerto_Engine]")
    exit(-1)

IP = argv[1]
PORT = int(argv[2])
run_socket()