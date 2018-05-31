from django.http import HttpResponse, HttpResponseRedirect
# modelos:
from .models import Museo
from .models import Comentario
from .models import Usuario
from .models import Seleccion
from django.contrib.auth.models import User

# for logout:
from django.contrib.auth.views import logout

from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import authenticate, login

# permisos post:
from django.views.decorators.csrf import csrf_exempt

# para el parser - udpdate:
from django.shortcuts import redirect
from .xml_parser_museos import parsear

from django.utils.datastructures import MultiValueDictKeyError
import math
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


FORM_LOGUEAR = """Iniciar sesion: <br>
				<form action="/" method="POST">
				Usuario: <input type="text" name="user"><br>
				<input type="hidden" name="option" value="sesion">
				Contraseña: <input type="password" name="pass"><br>
				<input type="submit" value="Entrar">
				</form>
				"""

MAX = 5  # num de museos en root page y en pag de usuario

def update(request):  # actualiza los contenidos y almacena en DB via RSS
	Museo.objects.all().delete()
	parsear()
	return redirect('/museos')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def mas_seleccionados(museos_DB):
	# 5 MUSEOS MAS SELECCIONADOS
	# Si no existen 5 => LOS MAS SELECCIONADOS
	lista = []  # lista de total de selecciones x museo
	for m in museos_DB:
		if m.selecciones>0:
			num = m.selecciones
			lista.append(num)

	total = len(lista)
	if total > 0:
		lista.sort(reverse=True) # de mayor a menor
	else:
		html = "No hay museos seleccionados"
		return html
	
	print("lista antes", lista)
	if total < MAX:
		lista = lista[0:total]
	else:
		lista = lista[0:MAX] # solo los 5 mas seleccionados

	html = ""
	mas = "Más información..."
	num = 0
	for m in museos_DB:
		if m.selecciones in lista and num < MAX:
			num = num + 1
			enlace_name = "<a href='" + m.link + "'>" + m.name + "</a><br>"
			html += enlace_name + m.direccion + " <a href\
			='/museos/" + str(m.id) + "'>" + mas + "</a><br><br>"
	return html


@csrf_exempt		
def root_page(request):
	html = "<html><head><h1>PAGINA PRINCIPAL - MUSEOS DE MADRID</h1></head><body>"
	if request.user.is_authenticated():
		logged = "Logged in as "+ request.user.username + ". <a href='/logout'>\
		Logout</a>"
		html += logged
	else:
		html += FORM_LOGUEAR

	if request.method == "GET":
		try:
			option = request.GET['option']
			if option == "accesibles": # MUSEOS ACCESIBLES
				museos_DB = Museo.objects.filter(access="1")
				html += BOTON_TODOS
			else: # TODOS
				museos_DB = Museo.objects.all()
				html += BOTON_ACCESIBLES

		except MultiValueDictKeyError:  # TODOS LOS MUSEOS
			museos_DB = Museo.objects.all()
			html += BOTON_ACCESIBLES
	else:  # HAN INICIADO SESION	
		user_name = request.POST['user']
		user_pass = request.POST['pass']
		autent = authenticate(username=user_name, password=user_pass)
		if autent is None:
			error = "ERROR AL INICIAR SESION"
			html += error
		else:
			login(request, autent)
		return HttpResponseRedirect('/')
		
	# 5 MUSEOS MAS SELECCIONADOS
	museos_mas = mas_seleccionados(museos_DB)
	html += museos_mas
	
	# PAGINAS PERSONALES DISPONIBLES
	pags_user = ""
	lista = []
	users_s = Seleccion.objects.all()
	for u in users_s:
		user_name = u.usuario.nombre
		title = u.usuario.titulo
		if user_name not in lista:
			if title == "":
				title = "Pagina de " + user_name
			pags_user += "<a href='" + user_name + "'>" + title + "</a><br>" + user_name + "<br>"
		lista.append(user_name)
	
	html += pags_user + "</body></html>"
	return HttpResponse(html)


def boton_seleccion(ide):
	html = "<form method='POST' action='/museos/'>\
			<input type='hidden' name='id_selecc' value='" + ide + "'>\
			<input type='submit' value='Seleccionar este museo'/>\
			</form>"
	return html


@csrf_exempt
def lista_museos(request):
	html = "<html><body>"
	ver_mas = "ver más..."
	nuevo_add = ""

	if request.user.is_authenticated():
		logged = "Logged in as "+ request.user.username + ". <a href='/logout'>\
		Logout</a>"
		html += logged + FORM_DISTRITO
	else:
		html += FORM_LOGUEAR + FORM_DISTRITO


	try: # GET
		distrito = request.GET['distrito']
		museos_DB = Museo.objects.filter(distrito=distrito)

	except MultiValueDictKeyError:  # no filtro
		museos_DB = Museo.objects.all()
	
	if request.method == "POST":  # Cuando seleccionan un MUSEO 
		ide = request.POST['id_selecc']
		museo_DB = Museo.objects.get(id=int(ide))
		user_name = User.objects.get(username=request.user.username) # users admin
		try: # es usuario que ya ha seleccionado
			usuario = Usuario.objects.get(nombre=user_name)
		except:  # si es su primera seleccion
			new_user = Usuario(nombre=user_name)
			new_user.save()
			usuario = Usuario.objects.all().last()
			new_selecc = Seleccion(museo=museo_DB, usuario=usuario)
			museo_DB.selecciones = museo_DB.selecciones + 1  # añadir seleccion a museo
			museo_DB.save()
			nuevo_add = "Nuevo museo " + museo_DB.name + " añadido!"
		
		try:  # museo ya seleccionado
			Seleccion.objects.get(museo=museo_DB, usuario=usuario)
			nuevo_add = "Museo " + museo_DB.name + " ya añadido."
		except:  # si no lo ha seleccionado antes
			
			new_selecc = Seleccion(museo=museo_DB, usuario=usuario)
			new_selecc.save()
			museo_DB.selecciones = museo_DB.selecciones + 1
			museo_DB.save()
			nuevo_add = "Nuevo museo " + museo_DB.name + " añadido!"
	
	html += nuevo_add
	for my_museo in museos_DB:
		html += ("<li>"+ my_museo.name + my_museo.access + 
		my_museo.distrito + "<a href='/museos/" + str(my_museo.id) + "'>" 
		+ ver_mas + "</a><br>")
		if request.user.is_authenticated():
			html += boton_seleccion(str(my_museo.id))
			
	html += "</body></html>"
	return HttpResponse(html)


def caja_comentario(ide):
	html = "<form action='/museos/" + ide + "' method='POST'>\
    		Escribe un comentario: <br><input type='text' name='comentario'\
    		value=''><br><input type='submit' value='Comentar'></form>"

	return (html)


@csrf_exempt
def pag_museo(request, ide):
	my_museo = Museo.objects.get(id=int(ide))

	html = "<html><body>"
	if request.user.is_authenticated():
		logged = "Logged in as "+ request.user.username + ". <a href='/logout'>\
		Logout</a>"
		html += logged + "<br><br>"
	else:
		html += FORM_LOGUEAR
	
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

	if request.user.is_authenticated():  # PUEDE COMENTAR
		form_comentario = caja_comentario(ide)
		html += form_comentario
		if request.method == "POST":
			texto = request.POST['comentario']
			new_comment = Comentario(texto=texto, museo=my_museo)
			new_comment.save()
			museo_redirect = "/museos/" + str(ide)
			return HttpResponseRedirect(museo_redirect)
			
	html += "</body></html>"
	return HttpResponse(html)

def caja_titulo(a_user):
	form_titulo = "<form action='/" + a_user + "/' method='POST'>\
    				Cambia el titulo de tu página!: \
    				<input type='text' name='titulo' value=''><br>\
    				<input type='hidden' name='option' value='1'>\
    				<input type='submit' value='Cambiar'>\
    				</form>"

	return form_titulo


def museos_seleccionados(a_user, pag):
	contenido = "Museos seleccionados por " + a_user + ": <br><br>"
	usuario = Usuario.objects.filter(nombre=a_user)
	total_s = Seleccion.objects.filter(usuario=usuario).count()
	fin_teorico = (int(pag)*MAX)-1 # 4, 9, 14 (cuando se seleccionan multiplos de 5 museos)
	inicio= fin_teorico-(MAX-1)
	if fin_teorico>total_s-1:
		fin_real = total_s-1
	else:
		fin_real = fin_teorico

	seleccionados = Seleccion.objects.filter(usuario=usuario)
	aux = 0
	for s in seleccionados:
		if aux>=inicio and aux<=fin_real:
			enlace_name = "<a href='" + s.museo.link + "'>" + s.museo.name + "</a><br>"
			contenido += enlace_name + s.museo.direccion
			contenido += " " + str(s.date) + "<br><br>"
		aux = aux + 1

	num_pags = math.ceil(total_s/MAX)  # redondea al entero superior
	print(total_s, num_pags)
	for i in range(num_pags):
		contenido += "<a href='/" + a_user + "=" + str(i+1) + "'>" + str(i+1) + "</a>"
		contenido += " "
	return contenido


def generar_titulo(a_user):
	try:
		usuario = Usuario.objects.get(nombre=a_user)
		if usuario.titulo != "":
			my_titulo = usuario.titulo
		else:
			my_titulo = "Pagina de " + a_user
	except: # si no ha seleccionado nada antes
		my_titulo = "Pagina de " + a_user
	
	return my_titulo


@csrf_exempt	
def pag_usuario(request, a_user):
	try:
		[a_user, pag] = a_user.split('=')
	except ValueError:
		pag = "1"
	print(a_user, pag)
	if request.method == "GET":
		form_titulo = ""
		if request.user.is_authenticated():
			logged = "Logged in as " + request.user.username + ".<a href\
			='/logout'>Logout</a>"
			try:
				user_logueado = request.user.username
				usuario = Usuario.objects.get(nombre=a_user)
				my_titulo = generar_titulo(a_user)
				if user_logueado == a_user:
					form_titulo = caja_titulo(a_user)
				contenido = museos_seleccionados(a_user, pag)
			except: # si no ha seleccionado nada antes
				print("Unexpected error:", sys.exc_info()[0])
				my_titulo = "Pagina de " + a_user
				  # no puede cambiar titulo
				contenido = "No tienes museos seleccionados"
		
		else:  # visitante que entra a la pagina de un usuario
			logged = FORM_LOGUEAR
			my_titulo = generar_titulo(a_user)
			contenido = museos_seleccionados(a_user, pag)

		html = ("<html><body>" + logged + "<br><h1>" + my_titulo + "</h1>" +
		form_titulo + contenido + "</html></body>")
		return HttpResponse(html)
		
	else: # POST
		# solo lo cambian usuarios logueados y que han seleccionado algun museo
		opcion = request.POST['option']
		if opcion == '1':
			new_titulo = request.POST['titulo']
			usuario = Usuario.objects.get(nombre=a_user)
			usuario.titulo = new_titulo
			usuario.save() 
			pag_user = "/" + a_user
			return HttpResponseRedirect(pag_user)
		else:
			return HttpResponse("ok") # PARA CAMBIAR CSS
		

