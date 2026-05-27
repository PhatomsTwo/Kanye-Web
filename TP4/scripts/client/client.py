import socket
import json
import base64
import time

HOST = "server"
PORT = 5000
XOR_KEY = "Yeezus"


def xor_bytes(data: bytes, key: bytes) -> bytes:
    if not key:
        raise ValueError("XOR_KEY must not be empty")
    return bytes(byte ^ key[index % len(key)] for index, byte in enumerate(data))


def encrypt_payload(text: str) -> str:
    raw = text.encode("utf-8")
    encrypted = xor_bytes(raw, XOR_KEY.encode("utf-8"))
    return base64.b64encode(encrypted).decode("ascii")

message = {
    "nombre": "KanyeWeb",
    "que_digo": "Boooouuuund 2 falling in looooove"
}

serialized_message = {
    "group": message["nombre"],
    "payload": encrypt_payload(message["que_digo"])
}

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        print("Intentando conectar al servidor..")
        client.connect((HOST, PORT))
        print("Conectado con éxito")
        break
    except ConnectionRefusedError:
        print("El servidor aún no acepta conexiones..")
        time.sleep(2)

client.sendall(json.dumps(serialized_message).encode("utf-8"))

client.close()