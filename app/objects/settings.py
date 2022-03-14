
class settings():
    def read_parametr(self, type='string', head='', parametr=''):
        # types
        #   bool
        #   float
        #   int
        #   string

        try:
            if type == 'bool':
                return True if (self.config.get(head, parametr)).lower() == 'true' else False
            
            elif type == "string":
                return (self.config.get(head, parametr))

        except Exception as e:
            print("Error read parametr: " + parametr + " in " + head + "(type: " + type + ")\n" + str(e))
            return None
            

    def __init__(self):
        self.path = 'settings.txt'
        self.config = configparser.ConfigParser()
        self.error = False

        # user
        self.name = "100LAR"

        # gui
        self.light_theme = False

        # chat
        self.save_history = True

        self.read_settings()

    def read_settings(self):
        if os.path.exists(self.path):
            self.config = configparser.ConfigParser()
            
            self.config.read(self.path)
            self.name = (self.read_parametr("string", "user", "name"))

            self.light_theme = (self.read_parametr("bool", "gui", "light_theme"))

            self.save_history = (self.read_parametr("bool", "chat", "save_history"))
        
        else:
            self.save_settings()

    def save_settings(self):
        self.config = configparser.ConfigParser()

        self.config.add_section("user")
        self.config.set("user", "name", str(self.name))

        self.config.add_section("gui")
        self.config.set("gui", "light_theme", str(self.light_theme))

        self.config.add_section("chat")
        self.config.set("chat", "save_history", str(self.save_history))

        with open(self.path, "w") as config_file: # запись файла с настройками
            self.config.write(config_file)