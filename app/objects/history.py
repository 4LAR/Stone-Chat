

class history():
    def __init__(self):
        self.path = 'history'
        # channel: [array]
        self.messages = {}

        self.read_history()

    def save_history(self):
        save_dict(self.messages, self.path)

    def read_history(self):
        try:
            self.messages = read_dict(self.path)
            return True

        except:
            return False


    def add_history_message(self, channel, message):
        try:
            self.messages[channel].append(message)
        except:
            self.messages[channel] = []
            self.messages[channel].append(message)

        self.save_history()

    def get_history(self, channel):
        try:
            return self.messages[channel]

        except:
            return []
    
    def history_clear(self, channel):
        self.messages[channel] = []
        self.save_history()

    def history_clear_all(self):
        self.messages = {}
        self.save_history()