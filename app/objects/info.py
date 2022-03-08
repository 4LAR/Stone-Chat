
class client_info():
    def __init__(self):
        self.update()

    def update(self):
        self.refresh()

    def refresh(self):
        self.ip = self.get_ip()
        self.name = self.get_name()
        self.mac = self.get_mac()

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def get_mac(self):
        address = hex(uuid.getnode())[2:]
        return '-'.join(address[i:i+2] for i in range(0, len(address), 2))

    def get_name(self):
        return socket.gethostname()
