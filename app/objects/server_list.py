
def save_dict(dict, name):
    json.dump(dict, open(str(name) + '.json','w'))

def read_dict(name):
    return json.load(open(str(name) + '.json'))

class server_list():
    def __init__(self):
        self.list = {}
        if not self.read_list():
            self.save_list()

    def add_server(self, ip, port, name):
        self.list[name] = {'ip': ip, 'port': port}
        self.save_list()

    def del_server(self, name):
        self.list.pop(name)
        self.save_list()

    def get_servers(self):
        return self.list

    def save_list(self):
        save_dict(self.list, 'servers')

    def read_list(self):
        try:
            self.list = read_dict('servers')
            return True

        except:
            return False
