import socket
import time
import os

os.system("ip route change default via 172.19.0.5")

HOST = "172.18.0.2"  # The server's hostname or IP address
PORT = 44445  # The port used by the server


def showPrices():
    print("Cool COFFEEMAKER", "SERVER:", HOST)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            s.sendall(b"\x01")
            data = s.recv(1024)
            action = data[0]
            if action == 1:
                priceLen = int((len(data) -1) / 9)
                for i in range(priceLen):
                    price = data[i * 9 + 1:i * 9 + 10]
                    name = price[0:8].decode("ascii").strip()
                    priceNumber = int.from_bytes(price[8:9], "little")
                    print(name, "costs", (priceNumber / 100), "€")
        except:
           print("Error")

while True:
    time.sleep(1)
    showPrices()