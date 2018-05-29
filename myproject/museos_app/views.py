from django.http import HttpResponse
from .models import Museo
from .models import Comentario

from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import authenticate

# permisos post:
from django.views.decorators.csrf import csrf_exempt

# para el parser - udpdate:
from django.shortcuts import redirect
from .xml_parser_museos import parsear

from django.utils.datastructures import MultiValueDictKeyError

import sys
# Create your views here.

BOTON_ACCESIBLES = """<form method="GET" action="/">
					<input type="hidden" name="option" value="accesibles">
					<input type="submit" value="Ver museos accesibles" />
					</form>"""


BOTON_TODOS = """<form method="" action="/">
				<input type="hidden" name="option" value="todos">
				<input type="submit" value="Ver todos los museos" />
				</form>"""
				

FORM_DISTRITO = """<form action="/museos" method="GET">
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
			
		#FALTA MUSEOS MAS SELECIONADOS 
	for my_museo in museos_DB:
		html += "<li>"+ my_museo.name + "<br>" + my_museo.direccion + "<a href\
		='/museos/" + str(my_museo.id) + "'>" + mas + "</a><br>"
	html += "</body></html>"
	return HttpResponse(html)


def lista_museos(request):
	html = "<html><body>" + FORM_DISTRITO
	ver_mas = "ver más..."
	if request.method == "GET":
		try:
			distrito = request.GET['distrito']
			museos_DB = Museo.objects.filter(distrito=distrito)

		except MultiValueDictKeyError:	
			museos_DB = Museo.objects.all()

		for my_museo in museos_DB:
			html += ("<li>"+ my_museo.name + my_museo.access + 
			my_museo.distrito + "<a href='/museos/" + str(my_museo.id) + "'>" 
			+ ver_mas + "</a><br>")
	else:  #POST PARA SELECCIONAR MUSEO
		print("museo seleccionado")
	html += "</body></html>"
	return HttpResponse(html)


def caja_comentario(ide):
	html = "<form action='/museos/" + ide + "' method='POST'>\
    		Escribe un comentario: <br><input type='text' name='comentario'\
    		value=''><br><input type='submit' value='Comentar'></form>"

	return (html)


@csrf_exempt
def un_museo(request, ide):
	my_museo = Museo.objects.get(id=int(ide))

	html = "<html><body>"
	html += my_museo.name + "<br>" + my_museo.descrip + "<br>ACCESIBLE: "
	html += my_museo.access + "<br>Enlace oficial: " + my_museo.link
	html += "<br> Direccion: " + my_museo.direccion + " - " + my_museo.barrio
	html += " - " + my_museo.distrito + "<br>Telefono: " + my_museo.telefono
	html += " Email: " + my_museo.email + "<br>"
	
	total_comments = Comentario.objects.filter(museo=my_museo).count()
	if total_comments != 0:
		comentarios = Comentario.objects.filter(museo=my_museo)
		comments = ""
		for a_comment in comentarios:
			comments += a_comment.texto + "<br>"
	else:
		comments = "No existen comentarios."
	
	html += comments
	#comentarios = "Hola COMENTARIO"
	if request.user.is_authenticated():  # PUEDE COMENTAR
		form_comentario = caja_comentario(ide)
		html += form_comentario
		if request.method == "POST":
			texto = request.POST['comentario']
			new_comment = Comentario(texto=texto, museo=my_museo)
			new_comment.save()
			museo_redirect = "/museos/" + str(ide)
			return redirect(museo_redirect)
			
	html += "</body></html>"
	return HttpResponse(html)

	
	
	
