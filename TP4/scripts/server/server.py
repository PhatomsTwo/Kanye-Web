import socket
import threading
import json
import base64

HOST = "0.0.0.0"
PORT = 5000
BUFFER_SIZE = 1024
XOR_KEY = "Yeezus"


def xor_bytes(data: bytes, key: bytes) -> bytes:
    if not key:
        raise ValueError("XOR_KEY must not be empty")
    return bytes(byte ^ key[index % len(key)] for index, byte in enumerate(data))


def decrypt_payload(encoded: str) -> str:
    encrypted = base64.b64decode(encoded.encode("ascii"))
    raw = xor_bytes(encrypted, XOR_KEY.encode("utf-8"))
    return raw.decode("utf-8", errors="replace")


def handle_client(client_socket, client_address):
    ip_address = client_address[0]

    print(f"Hello {ip_address} welcome to the server!")

    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE)

            if not data:
                break

            try:
                message = json.loads(data.decode("utf-8"))

                if (
                    isinstance(message, dict)
                    and "group" in message
                    and "payload" in message
                    and isinstance(message["group"], str)
                    and isinstance(message["payload"], str)
                ):
                    decrypted_payload = decrypt_payload(message["payload"])
                    print(f"{message['group']}: {decrypted_payload}")
                else:
                    print(f"{ip_address} wants to send an ill formatted message.")

            except json.JSONDecodeError:
                print(f"{ip_address} wants to send an ill formatted message.")

    except ConnectionResetError:
        pass

    finally:
        print(f"Bye {ip_address}!")
        client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()

            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )

            client_thread.start()

    except KeyboardInterrupt:
        print("\nServer stopped.")

    finally:
        server_socket.close()


if __name__ == "__main__":
    main()