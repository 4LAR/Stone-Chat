#
#
#	BOT >|<EKA
#
# [Stolar Studio]
#

import socket, threading, time, os

key = 8194

shutdown = False
join = False
def codem(message):

	crypt = ""; key = 8194
	for i in message:
		crypt += chr(ord(i)^key)
	message = crypt
	return message
def receving (name1, sock):
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
				#print(decrypt)
				name = ""
				decryptcmd = ""; k = False
				s1 = False; s2 = False
				for i in decrypt:
					if i == "]":
						s2 = True
					if s1 and not s2:
						name += i
					if i == "[":
						s1 = True
					
					
					if s1 and s2:
						decryptcmd += i
				decryptcmd = decryptcmd[5:]
				print(name+" > "+decryptcmd)

				if decryptcmd == "?help" :
					s.sendto(("["+alias + "] :: "+codem("?time")).encode("utf-8"),server)
				elif decryptcmd == "?time":
                                        s.sendto(("["+alias + "] :: "+codem(time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()))).encode("utf-8"),server)
				#message = name+" "+decryptcmd
				
				
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

print("BOT >|<EKA v0.1 [ Stolar Studio ]")
serverIP = input("Server IP : ")

serverPort = 8080
server = (serverIP, serverPort)

alias = "BOT >|<EKA"

rT = threading.Thread(target = receving, args = ("RecvThread",s))
rT.start()

while shutdown == False:
	if join == False:
		s.sendto(("["+alias + "] => join chat ").encode("utf-8"),server)
		print("["+alias + "] => join chat ")
		join = True
	else:
		try:
			
			com = input()
			if com == "/exit":
				s.sendto(("["+alias + "] <= left chat ").encode("utf-8"),server)
				print("["+alias + "] <= left chat ")
				shutdown = True
			time.sleep(0.2)
		except:
			if log:
				print("[ ERROR ]")
			#shutdown = True

rT.join()
s.close()

print("Press enter...")
input()
