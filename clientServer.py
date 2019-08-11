#
#	 Stone Chat
#       Client  v2.1
#
# [Stolar Studio]
#

import socket, threading, time, os, configparser

key = 8194

shutdown = False
join = False

config = configparser.ConfigParser()
config.read("client_settings.txt")
os_type = config.get("Settings", "os")
alias = config.get("Settings", "name")
key = config.get("Settings", "key")

def code(msg, key):
	crypt = ""
	for i in msg:
		crypt += chr(ord(i)^int(key))
	return crypt

def decode(message, key):
	decrypt = ""; k = False
	for i in message:
		if i == ":":
			k = True
			decrypt += i
		elif k == False or i == " ":
			decrypt += i
		else:
			decrypt += chr(ord(i)^int(key))
	return decrypt

def clrscr():
	if "1" in os_type:
		os.system("clear")
	elif "2" in os_type:
		os.system("cls")


def receving (name, sock):
	while not shutdown:
		try:
			while True:
				data, addr = sock.recvfrom(1024)
				print(decode(data.decode("utf-8"), key))
				time.sleep(0.2)
		except:
			pass
host = socket.gethostbyname(socket.gethostname())
port = 0

log = True

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0)

ver = "2.1"

clrscr()
print("\n Stone Chat Client "+ver+"\n")
serverIP = input("Server IP : ")
serverPort = input("Port : ")
clrscr()
server = (serverIP, int(serverPort))



aliasold = ""

rT = threading.Thread(target = receving, args = ("RecvThread",s))
rT.start()

while shutdown == False:
	if join == False:
		s.sendto(("["+alias + "] => join chat ").encode("utf-8"),server)
		print("["+alias + "] => join chat ")
		join = True
	else:
		try:
			message = input()
			if message[0] == "/":
				if message == "/exit":
					s.sendto(("["+alias + "] <= left chat ").encode("utf-8"),server)
					print("["+alias + "] <= left chat ")
					shutdown = True
				elif message == "/help":
					print("	COMMANDS");
					print(" /exit - выход с сервера")
					print(" /info - информация о клиенте")
					print(" /clear - очистка консоли")
					print("\n")
					print(" COMMANDS FOR ADMINS")
					print(" /stop - остановить сервер")
					print(" /clear log - очиска файла лога")
					print("\n")
				elif message == "/info":
					print("\n Stone Chat Client "+ver+"\n")
					print("[ IP Server : "+serverIP+ " ][ Your IP : "+host+" ]")
					print(" Your Name : "+alias)
					print("\n")
				elif message == "/stop" or message == "/clear log":
					s.sendto(("["+alias + "] :: "+code(message,key)).encode("utf-8"),server)
				elif message == "/clear":
					clrscr()
				else:
					print("[ ERROR COMMAND ]");
			else:
				if message != "":
					s.sendto(("["+alias + "] :: "+code(message,key)).encode("utf-8"),server)
				
				time.sleep(0.2)
		except:
			if log:
				print("[ ERROR ]")

rT.join()
s.close()

