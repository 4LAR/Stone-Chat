#
#	 Stone Chat
#       Server  v1.0
#
# [Stolar Studio]
#


import socket, time, os.path

host = socket.gethostbyname(socket.gethostname())
port = 8080

clients = []
users = []

#settings
printError = False

key = 8194

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))

quit = False
print("IP : " + host)
print("[ Server Started ]")

adminsIP = [host]
adminsName = ["admin"]

itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
f = open("log.txt", "a")
f.write("[" + itsatime + "]=[ Server Started ]\n")
f.close()

message = ""

while not quit:
	try:
		data, addr = s.recvfrom(1024)

		if addr not in clients:
			clients.append(addr)

		itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
		
		print("["+addr[0]+"]=["+str(addr[1])+"]=["+itsatime+"]/",end="")


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

		decryptcmd = ""; k = False
		for i in data.decode("utf-8"):
			if i == "=":
				k = True
				decryptcmd += i
			elif k == False or i == " ":
				decryptcmd += i
			else:
				decryptcmd += chr(ord(i)^key)
		#print(decryptcmd)
		
		for i in range(len(adminsIP)):
			if adminsIP[i] == addr[0]:
				for j in range(len(adminsName)):
					if decryptcmd == "[" + adminsName[j] + "] == /stop":
						quit = True
					elif decryptcmd == "[" + adminsName[j] + "] == /clear log":
						f = open("log.txt", "w")
						#f.write("[" + itsatime + "]=[ Clear Log ]\n")
						f.close()
						data = "[ Log Cleared ]"
						s.sendto(data.encode("utf-8"),addr)
                                                        
							
		f = open("log.txt", "a")
		f.write("["+addr[0]+"]=["+str(addr[1])+"]=["+itsatime+"]/"+decrypt+"\n")
		f.close()
			
		for client in clients:
			if addr != client:
				s.sendto(data,client)
	except:	
		#quit = True
		if printError:
			print("[ ERROR ]")
			itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
			f = open("log.txt", "a")
			f.write("[" + itsatime + "]=[ ERROR ]\n")

print("\n[ Server Stopped ]")
data = "[ Server Stopped ]"

for client in clients:
	s.sendto(data.encode("utf-8"),client)

itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
f = open("log.txt", "a")
f.write("[" + itsatime + "]=[ Server Stopped ]\n")

f.close()		
s.close()

input()
