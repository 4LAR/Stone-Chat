
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *

import os
import sys

import json

from info import *
info = client_info()

from net import *

def set_user_info():
    window.run_js(window.browser, "set_user_info('%s', '%s')" % (info.name, info.ip))

class WebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        global window
        global client

        print(message)
        if message == 'load':
            #window.run_js(window.browser, "add_message('admin', 'hello world')")
            window.load_page = True
            set_user_info()
        else:
            message_json = json.loads(str(message))
            client.send(message_json['message'])


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

    def append_message(self, message):
        print(1)
        self.run_js(self.browser, "add_message('%s', '%s')" % ('loh', message))

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.load_page = False

        self.setGeometry(100, 100, 1280, 720)
        self.setFixedSize(self.width(), self.height())

        self.browser = QWebEngineView(self)
        self.browser.setFixedSize(self.width(), self.height())
        self.browser.setUrl(QUrl("chrome://gpu/"))
        self.browser.setPage(WebEnginePage(self.browser))
        self.browser.setHtml(open('templates/main.html', 'r').read())
        self.loadCSS(self.browser, "static/main.css", "script1")

        self.browser.loadFinished.connect(self.update_title)
        #self.browser.move(200, 300)

        #self.run_js(self.browser, "add_message('admin', 'hello world')")


        self.show()

        self.setWindowIcon(QIcon('icon.png'))

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("%s" % title)

    def resizeEvent(self, event):
        pass
        '''
        self.browser.setZoomFactor(self.width() / (1920 + 55))
        self.browser.setFixedSize(self.width() - ((self.width() / 1920) * 55), self.height() - ((self.width() / 1920) * 55))

        self.browser_gui.setZoomFactor(self.width() / 1920)
        self.browser_gui.setFixedSize(self.width(), self.height())

        self.browser.move((self.width() / 1920) * 55, (self.width() / 1920) * 57)'''


os.environ[
        "QTWEBENGINE_CHROMIUM_FLAGS"
    ] = "--disable-web-security --ignore-gpu-blacklist --enable-gpu-rasterization --enable-smooth-scrolling"

os.environ[
        "QTWEBENGINE_REMOTE_DEBUGGING"
    ] = "9090"


app = QApplication(sys.argv)

app.setApplicationName("100LAR-WEB")
app.setOrganizationName("100LAR STUDIO")

window = MainWindow()

client = client()
#client.connect(info.ip, ["192.168.1.119", 8080])
#client.send("hello")

sys.exit(app.exec_())
