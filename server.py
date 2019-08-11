#
#	 Stone Chat
#       Server  v2.1
#
# [Stolar Studio]
#


import socket, time, os.path, configparser





def namew(msg):
	name = ""
	s1 = False; s2 = False
	for i in msg:
		if i == "]":
			s2 = True
		if s1 and not s2:
			name += i
		if i == "[":
		 	s1 = True
	return name

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

host = socket.gethostbyname(socket.gethostname())
port = 8080

white_list = "0"

clients = []
white_list_clients = []
users = []

ver = "2.1"

printError = False
vip = False
key = 8194

if not os.path.exists("server_settings.txt"):
	config = configparser.ConfigParser()
	config.add_section("Settings")
	config.set("Settings", "white-list", str(white_list))
	config.set("Settings", "port", str(port))
	config.set("Settings", "key", str(key))
	with open("server_settings.txt", "w") as config_file:
		config.write(config_file)
else:
	config = configparser.ConfigParser()
	config.read("server_settings.txt")
	white_list = config.get("Settings", "white-list")
	port = config.get("Settings", "port")
	key = config.get("Settings", "key")
	
if "1" in white_list:
	if os.path.exists("white_list.txt"):
		with open("white_list.txt") as f:
			clients = f.read().splitlines()
	else:
		f = open("white_list.txt", "w")
		f.close()

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,int(port)))

quit = False
print("\n Stone Chat Server "+ver+"\n")
print("IP : " + host)
print("Port : "+port)
print("\n[ Server Started ]")

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


		if "0" in white_list:
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


		for i in range(len(adminsIP)):
			if adminsIP[i] == addr[0]:
				for j in range(len(adminsName)):
					if adminsName[j] == namew(decrypt):
						data = "(admin)"+data.decode("utf-8")
						vip = True
					
		for client in clients:
			if addr != client:
				if vip:
					s.sendto(data.encode("utf-8"),client)
				else:
					s.sendto(data,client)
		vip = False
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
