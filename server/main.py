
import socket
import time 
import os

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

host = get_ip()
port = 8080

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,int(port)))

clients = []

run = True

print("\n Stone Chat Server \n")
print("IP : " + host)
print("Port : " + str(port))

while run:
    try:
        data, addr = s.recvfrom(1024)

        if addr not in clients:
            clients.append(addr)

        message = data.decode("utf-8")

        print(message)

        if message != "join":
            for client in clients:
                s.sendto(message.encode("utf-8"),client)

    except:
        pass
