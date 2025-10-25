import time
from sys import argv
import config
from socket import socket
import threading
from kafka_producer import send_stop_order, send_transaction_state
from kafka_consumer import receive_orders

def update_power():
    while True:
        if config.STATE == config.STATES["SUMINISTRANDO"]:
            print("MANDANDO TRANSACCION....")
            send_transaction_state()
            config.REMAINING_POWER -= 1
            config.TOTAL_CHARGED += 1
            time.sleep(1)
            if config.REMAINING_POWER <= 0:
                config.REMAINING_POWER = 0
                config.STATE = config.STATES["FUERA DE SERVICIO"]


def get_ko():
    while True:
        if config.STATE == config.STATES["K.O."]:
            message = input("[Engine] Presione una tecla para recuperar el CP: ")
            if message:
                config.STATE = config.STATES["ACTIVO"]
        else:
            message = input("[Engine] Presione una tecla para mandar un K.O: ")
            if message:
                config.STATE = config.STATES["K.O."]

def handle_monitor(connection):
    while True:
        msg = connection.recv(1)
        if not msg:
            print("[Engine] El monitor cerró la conexión")
            break
        if msg == b'\x01':
            config.STATE = config.STATES["SUMINISTRANDO"]
        elif msg == b'\x00' and config.STATE == config.STATES["SUMINISTRANDO"]:
            send_stop_order()
            config.TOTAL_CHARGED = 0
            config.PAIRED = ""
            config.STATE = config.STATES["ACTIVO"]
        else:
            config.STATE = config.STATES["ACTIVO"]

        connection.send(config.STATE)
        payload = f"{config.PAIRED}#{config.REMAINING_POWER}#{config.TOTAL_CHARGED}".encode()
        connection.send(payload)
    connection.close()

if len(argv) < 5:
    print("Uso: EV_CP_E [Puerto] [IP Kafka] [Puerto Kafka] [Identificador]")
    exit(-1)

config.PORT = int(argv[1])
config.BROKER_IP = argv[2]
config.BROKER_PORT = int(argv[3])
config.CP_ID = argv[4]

s = socket()
s.bind(('', config.PORT))
s.listen(5)
print("[Engine] Escuchando en el puerto " + str(config.PORT))

ko_thread = threading.Thread(target=get_ko, daemon=True)
ko_thread.start()

kafka_thread = threading.Thread(target=receive_orders, daemon=True)
kafka_thread.start()

update_thread = threading.Thread(target=update_power, daemon=True)
update_thread.start()

while True:
    connection, addr = s.accept()
    handler = threading.Thread(target=handle_monitor, args=[connection], daemon=True)
    handler.start()