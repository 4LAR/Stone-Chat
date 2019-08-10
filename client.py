#
#	 Stone Chat
#       Client  v1.0
#
# [Stolar Studio]
#

import socket, threading, time, os

key = 8194

shutdown = False
join = False

def receving (name, sock):
	while not shutdown:
		try:
			while True:
				data, addr = sock.recvfrom(1024)
				#print(data.decode("utf-8"))
				# Begin расшифрование
				decrypt = ""; k = False
				for i in data.decode("utf-8"):
					if i == ":":
						k = True
						decrypt += i
					elif k == False or i == " ":
						decrypt += i
					else:
						decrypt += chr(ord(i)^key)
				print(decrypt)
				
				# End

				time.sleep(0.2)
		except:
			pass
host = socket.gethostbyname(socket.gethostname())
port = 0

log = False

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0)

ver = "1.1"

print("\n Stone Chat Client "+ver+"\n")
serverIP = input("Server IP : ")

serverPort = 8080
server = (serverIP, serverPort)

alias = input("Name: ")
print("\n")
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
					print(" /rename - изменить имя")
					print(" /info - информация о клиенте")
					print(" /clear w - очистка консоли если у вас windows")
					print(" /clear l - очистка консоли если у вас linux")
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
				elif message == "/rename":
					aliasold = alias
					alias = input("New name : ")
					s.sendto(("["+alias + "] "+ aliasold +" rename to " + alias).encode("utf-8"),server)
				elif message == "/stop":
					crypt = ""
					for i in message:
						crypt += chr(ord(i)^key)
					message = crypt
					s.sendto(("["+alias + "] == "+message).encode("utf-8"),server)
				elif message == "/clear log":
					crypt = ""
					for i in message:
						crypt += chr(ord(i)^key)
					message = crypt
					s.sendto(("["+alias + "] == "+message).encode("utf-8"),server)
				elif message == "/clear w":
					os.system("cls")
					print("\n Stone Chat Client "+ver+"\n")
				elif message == "/clear l":
					os.system("clear")
					print("\n Stone Chat Client "+ver+"\n")
				else:
					print("[ ERROR COMMAND ]");
			else:
				# Begin шифрование
				crypt = ""
				for i in message:
					crypt += chr(ord(i)^key)
				message = crypt
				# End
				if message != "":
					s.sendto(("["+alias + "] :: "+message).encode("utf-8"),server)
				
				time.sleep(0.2)
		except:
			if log:
				print("[ ERROR ]")
			#shutdown = True

rT.join()
s.close()

print("Press enter...")
input()
