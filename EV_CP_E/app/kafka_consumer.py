import time

from kafka import KafkaConsumer
import config
from json import loads

consumer = None
try:
    print(f"[KafkaConsumer] Intentando conectar con Kafka ({config.BROKER_IP}:{config.BROKER_PORT})...")
    consumer = KafkaConsumer(
        "orders",
        bootstrap_servers=[f"{config.BROKER_IP}:{config.BROKER_PORT}"],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda m: loads(m.decode('utf-8'))
    )
    print("[KafkaConsumer] Conectado a Kafka")
except:
    print("[KafkaConsumer] Error al conectar con Kafka")

def receive_orders():
    while True:
        if not consumer:
            time.sleep(5)
            continue
        for message in consumer:
            data = message.value
            ordertype = data.get("type")
            source = data.get("from")
            destination = data.get("to")
            if source != config.CP_ID:
                continue
            if ordertype == "prepare":
                config.TOTAL_CHARGED = 0
                config.PAIRED = destination
            time.sleep(1)
