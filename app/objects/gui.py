
def set_user_info():
    window.run_js(window.browser, "set_user_info('%s', '%s', '%s', '%s')" % (settings.name, info.name, info.ip, info.mac))

def load_servers():
    window.run_js(window.browser, "clear_server_list()")
    list = server_list.get_servers()
    for serv in list:
        window.run_js(window.browser, "add_server('%s', '%s', '%s')" % (serv, list[serv]['ip'], list[serv]['port']))

def load_settings():
    settings_dict = {
        "name": settings.name,
        "light_theme": settings.light_theme,
        "save_history": settings.save_history

    }
    settings_json = json.dumps(settings_dict)
    window.run_js(window.browser, "read_settings('%s')" % (settings_json))


class WebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        global window
        global client

        print(message)
        if message == 'load':
            window.load_page = True
            set_user_info()
            load_servers()
            load_settings()
            window.run_js(window.browser, "chat_go_down()")

        elif message == 'exit':
            window.close()

        elif message.split("|")[0] == 'add_server':
            message_json = json.loads(str(message.split("|")[1]))
            server_list.add_server(message_json['ip'], message_json['port'], message_json['name'])
            load_servers()

        elif message.split("|")[0] == 'connect_to_server':
            message_json = json.loads(str(message.split("|")[1]))
            client.disconnect()
            client.connect(info.ip, [message_json['ip'], int(message_json['port'])])

        elif message.split("|")[0] == 'save_settings':
            message_json = json.loads(str(message.split("|")[1]))

            settings.name = message_json['name']
            settings.light_theme = message_json['light_theme']
            settings.save_history = message_json['save_history']

            settings.save_settings()

        else:
            #message_json = json.loads(str(message))
            client.send(message)


class MainWindow(QMainWindow):
    def loadCSS(self, view, path, name):
        path = QFile(path)
        if not path.open(QFile.ReadOnly | QFile.Text):
            print("ERROR READ")
            return
        css = path.readAll().data().decode("utf-8")
        SCRIPT = """
        (function() {
        css = document.createElement('style');
        css.type = 'text/css';
        css.id = "%s";
        document.head.appendChild(css);
        css.innerText = `%s`;
        })()
        """ % (name, css)

        script = QWebEngineScript()
        view.page().runJavaScript(SCRIPT, QWebEngineScript.ApplicationWorld)
        script.setName(name)
        script.setSourceCode(SCRIPT)
        script.setInjectionPoint(QWebEngineScript.DocumentReady)
        script.setRunsOnSubFrames(True)
        script.setWorldId(QWebEngineScript.ApplicationWorld)
        view.page().scripts().insert(script)

    def run_js(self, view, function=''):
        view.page().runJavaScript(function)

    def append_message(self, name, message, data):

        self.run_js(self.browser, "add_message('%s', '%s', '%s')" % (name, message, data))

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.load_page = False

        self.setGeometry(100, 100, 1280, 720)
        self.setMinimumSize(640, 480)
        #self.setFixedSize(self.width(), self.height())

        self.browser = QWebEngineView(self)
        self.browser.setFixedSize(self.width(), self.height())
        self.browser.setUrl(QUrl("chrome://gpu/"))
        self.browser.setPage(WebEnginePage(self.browser))
        self.browser.setHtml(open('templates/main.html', 'r').read())
        self.loadCSS(self.browser, "static/main.css", "main_style")
        self.loadCSS(self.browser, "static/slider.css", "slider_style")

        self.browser.loadFinished.connect(self.update_title)

        self.show()

        self.setWindowIcon(QIcon('icon.png'))

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("%s" % title)

    def resizeEvent(self, event):
        self.browser.setFixedSize(self.width(), self.height())

    def closeEvent(self,event):
        global client
        client.disconnect()


os.environ[
        "QTWEBENGINE_CHROMIUM_FLAGS"
    ] = "--disable-web-security --ignore-gpu-blacklist --enable-gpu-rasterization --enable-smooth-scrolling"

os.environ[
        "QTWEBENGINE_REMOTE_DEBUGGING"
    ] = "9090"
