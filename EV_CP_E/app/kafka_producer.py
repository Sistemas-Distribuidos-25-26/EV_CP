from kafka import KafkaProducer
import config
import json

producer = None
try:
    print(f"[KafkaProducer] Intentando conectar con Kafka ({config.BROKER_IP}:{config.BROKER_PORT})...")
    producer = KafkaProducer(
        bootstrap_servers = [f"{config.BROKER_IP}:{config.BROKER_PORT}"],
        value_serializer= lambda  v: json.dumps(v).encode("utf-8")
    )
    print("[KafkaProducer] Conectado a Kafka")
except Exception as e:
    print(e)
    producer=None

def send_transaction_state():
    if not producer: return
    producer.send("transactions", {
        "cp": config.CP_ID,
        "paired": config.PAIRED,
        "total_charged": config.TOTAL_CHARGED
    })

def send_stop_order():
    if not producer: return
    producer.send("orders", {
        "type": "stop",
        "from": config.CP_ID,
        "to": config.PAIRED
    })