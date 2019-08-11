#
#	 Stone Chat
#       Server  v2.0
#
# [Stolar Studio]
#


import socket, time, os.path

host = socket.gethostbyname(socket.gethostname())
port = 8080

clients = []
users = []

ver = "2.0"

#settings
printError = False

key = 8194


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


s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))

quit = False
print("\n Stone Chat Server "+ver+"\n")
print("IP : " + host)
print("[ Server Started ]")

adminsIP = []
adminsName = []

if os.path.exists("adminsIP.txt"):
	with open("adminsIP.txt") as f:
		adminsIP = f.read().splitlines()
else:
	f = open("adminsIP.txt", "w")
	f.write(host)
	f.close()
	adminsIP = [host]
	
if os.path.exists("adminsName.txt"):
	with open("adminsName.txt") as f:
		adminsName = f.read().splitlines()
else:
	f = open("adminsName.txt", "w")
	f.write("admin\n")
	f.close()
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

		decrypt = decode(data.decode("utf-8"), key)
		
		print(decrypt)
		
		for i in range(len(adminsIP)):
			if adminsIP[i] == addr[0]:
				for j in range(len(adminsName)):
					if decrypt == "[" + adminsName[j] + "] :: /stop":
						quit = True
					elif decrypt == "[" + adminsName[j] + "] :: /clear log":
						f = open("log.txt", "w")
						f.write("[" + itsatime + "]=[ Clear Log ]\n")
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
