app = QApplication(sys.argv)

info = client_info()
settings = settings()
server_list = server_list()

app.setApplicationName("100LAR-WEB")
app.setOrganizationName("100LAR STUDIO")

window = MainWindow()

client = client()
client.connect(info.ip, ["192.168.43.218", 8080])
#client.send("hello")

sys.exit(app.exec_())
