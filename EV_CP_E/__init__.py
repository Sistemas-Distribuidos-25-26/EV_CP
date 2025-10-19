import time
from sys import argv
import config
from socket import socket
import threading

from kafka_consumer import receive_orders

def update_power():
    while True:
        if config.STATE == config.STATES["CHARGING"]:
            config.REMAINING_POWER -= 0.1
            time.sleep(0.1)
            if config.REMAINING_POWER <= 0:
                config.REMAINING_POWER = 0
                config.STATE = config.STATES["OUT_OF_ORDER"]


def get_ko():
    while True:
        if config.STATE == config.STATES["BROKEN"]:
            message = input("[Engine] Presione una tecla para recuperar el CP: ")
            if message:
                config.STATE = config.STATES["ACTIVE"]
        else:
            message = input("[Engine] Presione una tecla para mandar un K.O: ")
            if message:
                config.STATE = config.STATES["BROKEN"]

def handle_monitor(connection):
    while True:
        msg = connection.recv(1)
        if not msg:
            print("[Engine] El monitor cerró la conexión")
            break
        connection.send(config.STATE)
    connection.close()

if len(argv) < 5:
    print("Uso: EV_CP_E [Puerto] [IP Kafka] [Puerto Kafka] [Identificador]")
    exit(-1)

config.PORT = int(argv[1])
config.BROKER_IP = argv[2]
config.BROKER_PORT = int(argv[3])
config.CP_ID = argv[4]

s = socket()
s.bind(('',config.PORT))
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