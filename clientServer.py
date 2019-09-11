#
#	 Stone Chat
#        [Client]
#
# [Stolar Studio]
#

ver = "2.3"

import socket, threading, time, os, configparser

key = 8194

shutdown = False
join = False

config = configparser.ConfigParser()
config.read("client_settings.txt")
os_type = config.get("Settings", "os")
alias = config.get("Settings", "name")
key = config.get("Settings", "key")
enc_type = config.get("Settings", "encryption")
def ascii_code(msg, sc = 1, simv = " "):
    crypt = ""
    for j in range(int(sc)):
        for i in msg:
            crypt += str(ord(i))+simv
        msg = crypt; crypt = ""
    return msg
def ascii_decode(msg, sc = 1, simv = " "):
    dec_buf = ""; decode = ""
    for j in range(int(sc)):
        for i in msg:
            if i == simv:
                decode += chr(int(dec_buf))
                dec_buf = ""
            else:
                dec_buf += i
        msg = decode; decode = ""
    return msg
def ascii_plus_code(msg):
    msg = ascii_code(msg,2,"/")
    crypt = ""
    for i in msg:
        if not i == "/":
            crypt += i
    return crypt
def ascii_plus_decode(msg):
    j = 0; decrypt = ""
    for i in msg:
        j += 1
        decrypt += i
        if j == 2:
            decrypt += "/"
            j = 0
    return ascii_decode(decrypt, 2, "/")
def code_key(msg, key):
	crypt = ""
	for i in msg:
		crypt += chr(ord(i)^int(key))
	return crypt

def decode_key(message, key):
	decrypt = ""; k = False;decrypt_ascii = ""
	for i in message:
		if i == ":":
			k = True
			decrypt += i
		elif k == False or i == " ":
			decrypt += i
		else:
			decrypt += chr(ord(i)^int(key))
			decrypt_ascii += chr(ord(i)^int(key))
	if enc_type == "2":
		decrypt_ascii = ascii_decode(decrypt_ascii, 1, "/")
		if decrypt_ascii[:7] == "<ASCII>":
			decrypt = decrypt_ascii[7:]
	elif enc_type == "3":
		decrypt_ascii = ascii_plus_decode(decrypt_ascii)
		if decrypt_ascii[:8] == "<ASCII+>":
			decrypt = decrypt_ascii[8:]
	return decrypt
	
def code(msg):
	if enc_type == "0":
		return msg
	elif enc_type == "1":
		return code_key(msg,key)
	elif enc_type == "2":
		return code_key(ascii_code("<ASCII>"+msg,1,"/"),key)
	elif enc_type == "3":
		return code_key(ascii_plus_code("<ASCII+>"+msg),key)
def decode(msg):
	if enc_type == "0":
		return msg
	else:
		return decode_key(msg,key)
    
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
				print(decode(data.decode("utf-8")))
				time.sleep(0.2)
		except:
			pass
			
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip
			
#host = socket.gethostbyname(socket.gethostname())
host = get_ip() 
port = 0

log = True
    
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0)

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
					s.sendto(("["+alias + "] :: "+code(message)).encode("utf-8"),server)
				elif message == "/clear":
					clrscr()
				else:
					print("[ ERROR COMMAND ]");
			else:
				if message != "":
					s.sendto(("["+alias + "] :: "+code(message)).encode("utf-8"),server)
				
				time.sleep(0.2)
		except:
			if log:
				print("[ ERROR ]")

rT.join()
s.close()

