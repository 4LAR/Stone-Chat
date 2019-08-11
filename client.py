#
#	 Stone Chat
#       Client  v2.1
#
# [Stolar Studio]
#
#https://python-scripts.com/configparser-python-example

import socket, threading, time, os, os.path, configparser

ver = "2.1"

name = "user"
key = 8194

shutdown = False
join = False



log = True


def clrscr():
	if "1" in os_type:
		os.system("clear")
	elif "2" in os_type:
		os.system("cls")
		

		
def save_set() :
	config = configparser.ConfigParser()
	config.add_section("Settings")
	config.set("Settings", "os", str(os_type))
	config.set("Settings", "name", str(name))
	config.set("Settings", "key", str(key))
	with open("client_settings.txt", "w") as config_file:
		config.write(config_file)

if not os.path.exists("client_settings.txt"):
	
	print("	OS")
	print("1)Linux")
	print("2)Windows")
	os_type = input(">")
	if not "1" in os_type and not "2" in os_type:
		exit()
	clrscr()
	name = input("You name : ")
	clrscr()
	
	save_set()
else:
	config = configparser.ConfigParser()
	config.read("client_settings.txt")

	os_type = config.get("Settings", "os")
	name = config.get("Settings", "name")
	key = config.get("Settings", "key")
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
		if "0" in str(com):
			break
		elif "3" in str(com):
			while True:
				clrscr()
				print("	SETTINGS\n")
				
				print("1) OS : ", end = "")
				if "1" in os_type:
					print("Linux")
				elif "2" in os_type:
					print("Windows")
				print("2) Name : "+name)

				print("\n0)exit")
				#print()
				
				com = input("\n>")
				if "0" in str(com):
					break
				elif "1" in str(com):
					clrscr()
					print("\n1)Linux")
					print("2)Windows")
					com = input("\n>")
					if "1" in str(com) or "2" in str(com):
						os_type = com
				elif "2" in str(com):
					clrscr()
					name = input("\nNew name : ")
					
				save_set()
				
		elif "1" in str(com):
			if "1" in os_type:
				os.system("python3 clientServer.py")
			elif "2" in os_type:
				os.system("py clientServer.py")
			
	except:
		if log:
			print("ERROR")
			input()




print("\nPress enter...")
input()
