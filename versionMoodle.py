#!/usr/bin/python3.4

"""
# Mediante este programa se busca en los datos obtenidos de una pagina de moodle la version. 
# Busca un patron dentro de la pagina de administrador que es donde normalmente estan los datos
# 
#
# Autores:
# Yeudiel Hernandez Torres
# Ivan Hernandez Reyes
"""
from html.parser import HTMLParser
import requests
import re

def versionMoodle(url):
		
	try:

		resp = requests.get(url)
		if (resp.status_code == 200):
			print ("conectado")

		else:
			print (resp.status_code)
	except:
		print ("algo salio mal")
	return resp.text

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if (tag == 'a'):
        	for attr in attrs:
        		print (attr[1])
        		

    def handle_data(self, data):
    	
    		return data
        	
        

 
# URL donde buscar la version
#Por defaul buscara en una url de este tipo
url= "https://moodle.org/admin/index.php"

#hacer una petición para obtener los datos donde buscar
con = versionMoodle(url)

#crear un objeto para parsear
parser = MyHTMLParser()
#obtener los posibles espacios donde se encuentra
resultado = parser.handle_data(con)
#Volver a parsear para obtener solo los datos
busca = parser.handle_data(resultado)
#Buscar el patron de version Moodle X.X
patron = re.search('(Moodle \d\.\d)', busca)

print (patron.group(0))
