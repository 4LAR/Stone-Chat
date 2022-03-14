
import socket
import time
import os
import json
import threading
import sys

def get_time(): # получить текущее время
    return time.strftime("%H:%M %d-%m-%y", time.localtime())

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
print()

# поток для ввода
def console():
    global run
    global s

    global clients

    while run:
        try:
            command = input(" >> ")

            if command == 'exit':
                run = False
                s.shutdown(socket.SHUT_RDWR)

            elif command == 'clients':
                if len(clients) > 0:
                    for client in clients:
                        print(client)
                else:
                    print("no clients")
            else:
                print("Error command")

        except:
            pass

thread_console = threading.Thread(target = console)
thread_console.start()

while run:
    try:
        data, addr = s.recvfrom(1024)

        if addr not in clients:
            clients.append(addr)

        message = data.decode("utf-8")

        print(message)

        if message == "join":
            s.sendto("ok".encode("utf-8") ,addr)
            
        else:

            message = json.loads(str(message))
            message['data'] = get_time()
            message = json.dumps(message)
            
            for client in clients:
                s.sendto(message.encode("utf-8"),client)

    except:
        pass
