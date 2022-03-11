
messages = []

connected = False
def receving_thread_func(name, sock):
    global connected
    global messages

    print(connected)
    global window
    while connected:
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                messages.append(data.decode("utf-8"))
                print(data.decode("utf-8"))
                time.sleep(0.2)
                try:
                    message_json = json.loads(str(data.decode("utf-8")))
                    window.append_message(message_json['name'], message_json['message'])
                except Exception as e:
                    print(e)

        except Exception as e:
            pass
            #print("[ ERROR ] RECEVE: ", e)

def send_thread_func(name, sock, server, message):
    global window
    global info

    try:
        sock.sendto((message).encode("utf-8"), server)
        #window.append_message(info.name, message)
    except Exception as e:
        print("[ ERROR ] SEND: ", e)


class client():
    def __init__(self):
        # статус подключения
        self.connected = False

        # поток для получения данных
        self.thread_receving = None

        # поток для отправки
        self.thread_send = None

        self.sock = None
        self.server = None

    def connect(self, user_ip, addr):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.bind((user_ip, 0))
        self.server = (addr[0], int(addr[1]))
        self.sock.setblocking(0)

        global connected

        self.connected = True
        connected = True

        self.thread_receving = threading.Thread(target = receving_thread_func, args = ("receve", self.sock))
        self.thread_receving.start()

        self.send("join")

        print("CONNECTED to %s" % addr[0] + ':' + str(addr[1]))

    def send(self, message):
        if self.connected:
            self.thread_send = threading.Thread(target = send_thread_func, args = ("send", self.sock, self.server, message))
            self.thread_send.start()

    def disconnect(self):
        global connected

        self.connected = False
        connected = False

        print("DISCONNECTED")
