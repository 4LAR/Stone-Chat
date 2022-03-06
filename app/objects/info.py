
class client_info():
    def __init__(self):
        self.update()

    def update(self):
        self.ip = self.get_ip()
        self.name = self.get_name()

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

    def get_name(self):
        return socket.gethostname()
