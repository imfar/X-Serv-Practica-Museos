from django.shortcuts import render
from django.http import HttpResponse
from .models import Museo
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import authenticate

from django.views.decorators.csrf import csrf_exempt

# para el parser - udpdate:
from django.shortcuts import redirect
from xml.sax import make_parser
from .xml_parser_museos import parsear
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.

BOTON_ACCESIBLES = """<form method="get" action="/">
					<input type="hidden" name="option" value="accesibles">
					<input type="submit" value="Ver museos accesibles" />
					</form>"""


BOTON_TODOS = """<form method="get" action="/">
				<input type="hidden" name="option" value="todos">
				<input type="submit" value="Ver todos los museos" />
				</form>"""
				

BOTON_DISTRITO = """<form action="/museos" method="GET">
    				Distrito:<br>
    				<input type="text" name="distrito" value=""><br>
    				<input type="submit" value="Filtrar">
    				</form>"""


def update(request):  # actualiza los contenidos y almacena en DB via RSS
	Museo.objects.all().delete()
	parsear()
	return redirect('/museos')

@csrf_exempt		
def root_page(request):
	mas = "Más información..."
	try:
		option = request.GET['option']
		if option == "accesibles": # MUSEOS ACCESIBLES
			museos_DB = Museo.objects.filter(access="1")
			html = "<html><body>" + BOTON_TODOS
		else: # TODOS
			museos_DB = Museo.objects.all()
			html = "<html><body>" + BOTON_ACCESIBLES

	except MultiValueDictKeyError:
		museos_DB = Museo.objects.all()
		html = "<html><body>" + BOTON_ACCESIBLES
			
		#FALTA MUSEOS MAS SELECIONADOS Y QUE EL LINK SEA A MUSEOS/ID
	for my_museo in museos_DB:
		html += "<li>"+ my_museo.name + "<br>" + my_museo.direccion + "<a href='/museos/" + str(my_museo.id) + "'>" + mas + "</a><br>"
	html += "</body></html>"
	return HttpResponse(html)


def lista_museos(request):
	html = "<html><body>" + BOTON_DISTRITO
	ver_mas = "ver más..."
	if request.method == "GET":
		try:
			distrito = request.GET['distrito']
			museos_DB = Museo.objects.filter(distrito=distrito)

		except MultiValueDictKeyError:	
			museos_DB = Museo.objects.all()

		for my_museo in museos_DB:
			html += "<li>"+ my_museo.name + my_museo.access + my_museo.distrito + "<a href='/museos/" + str(my_museo.id) + "'>" + ver_mas + "</a><br>"
	else:  #POST PARA SELECCIONAR MUSEO
		print("museo seleccionado")
	html += "</body></html>"
	return HttpResponse(html)


def un_museo(request, ide):
	my_museo = Museo.objects.get(id=int(ide))
	html = "<html><body>"
	html += my_museo.name + "<br>" + my_museo.descrip + "<br>ACCESIBLE: "
	html += my_museo.access + "<br>Enlace oficial: " + my_museo.link
	html += "<br> Direccion: " + my_museo.direccion + " - " + my_museo.barrio
	html += " - " + my_museo.distrito + "<br>Telefono: " + my_museo.telefono
	html += " Email: " + my_museo.email
	html += "</body></html>"
	#FALTA LOS COMENTARIOS
	return HttpResponse(html)
	
	
	
	
