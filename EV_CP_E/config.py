

STATES = {
    "UNKNOWN": b'\x00',
    "ACTIVE": b'\x01',
    "OUT_OF_ORDER": b'\x02',
    "CHARGING": b'\x03',
    "BROKEN": b'\x04'
}

PORT : int = 5000
STATE = STATES["ACTIVE"]


BROKER_IP = "127.0.0.1"
BROKER_PORT = 9092

CP_ID = "CP000"

REMAINING_POWER = 50
PRICE = 0.34