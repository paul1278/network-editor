import socket
import os

os.system("ip route change default via 172.18.0.5")

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 44445  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                action = data[0]
                if action == 1:
                    print("Handing out the prices")
                    conn.sendall(b"\x01KAFFEE  \x64KAKAO   \x96")