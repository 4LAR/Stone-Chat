#
#	 Stone Chat
#        [Launcher]
#
# [Stolar Studio]
#

import socket, threading, time, os, os.path, configparser

ver = "2.2"

name = "user"
key = 8194
enc_type = "0"

shutdown = False
join = False



log = True


def clrscr():
	if "1" == os_type:
		os.system("clear")
	elif "2" == os_type:
		os.system("cls")
		

		
def save_set() :
	config = configparser.ConfigParser()
	config.add_section("Settings")
	config.set("Settings", "os", str(os_type))
	config.set("Settings", "name", str(name))
	config.set("Settings", "key", str(key))
	config.set("Settings", "encryption", str(enc_type))
	with open("client_settings.txt", "w") as config_file:
		config.write(config_file)

if not os.path.exists("client_settings.txt"):
	
	print("	OS")
	print("1)Linux")
	print("2)Windows")
	os_type = input(">")
	if not "1" == os_type and not "2" == os_type:
		exit()
	clrscr()
	com = input("You name : ")
	if len(com) > 0:
		name = com
	clrscr()
	
	save_set()
else:
	config = configparser.ConfigParser()
	config.read("client_settings.txt")

	os_type = config.get("Settings", "os")
	name = config.get("Settings", "name")
	key = config.get("Settings", "key")
	enc_type = config.get("Settings", "encryption")
while True:
	try:
		clrscr()
		print("\n Stone Chat "+ver+"\n")
		print("User : "+name+"\n")
		print("1)Join server")
		print("2)Join local (not ready)")
		print("3)settings")
		print("\n0)exit")
		com = input("\n>")
		if "0" == str(com):
			break
		elif "3" == str(com):
			while True:
				clrscr()
				print("	SETTINGS\n")
				
				print("1) OS : ", end = "")
				if "1" in os_type:
					print("Linux")
				elif "2" in os_type:
					print("Windows")
				print("2) Name : "+name)
				print("3) Encryption : ", end="")
				if enc_type == "0":
					print("nothing")
				elif enc_type == "1":
					print("KEY")
				elif enc_type == "2":
					print("KEY + ASCII")
				elif enc_type == "3":
					print("KEY + ASCII+")
				print("\n0)exit")
				#print()
				
				com = input("\n>")
				if "0" == str(com):
					break
				elif "1" == str(com):
					clrscr()
					print("\n1)Linux")
					print("2)Windows")
					com = input("\n>")
					if "1" in str(com) or "2" in str(com):
						os_type = com
				elif "2" == str(com):
					clrscr()
					com = input("\nNew name : ")
					if len(com) > 0:
						name = com
				elif "3" == str(com):
					clrscr()
					print("\n0)Nothing")
					print("1)KEY")
					print("2)ASCII")
					print("3)ASCII+")
					com = input("\n>")
					if "1" in str(com) or "2" in str(com) or "3" in str(com) or "0" in str(com):
						enc_type = com
				save_set()
				
		elif "1" == str(com):
			if "1" == os_type:
				os.system("python3 clientServer.py")
			elif "2" == os_type:
				os.system("py clientServer.py")
			
	except:
		if log:
			print("ERROR")
			input()




print("\nPress enter...")
input()
