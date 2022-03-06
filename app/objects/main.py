app = QApplication(sys.argv)

app.setApplicationName("100LAR-WEB")
app.setOrganizationName("100LAR STUDIO")

window = MainWindow()

client = client()
client.connect(info.ip, ["192.168.1.119", 8080])
#client.send("hello")

sys.exit(app.exec_())
