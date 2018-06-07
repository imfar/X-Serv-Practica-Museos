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
import json

# Create your views here.

BOTON_ACCESIBLES = """<center><form method="GET" action="/">
					<input type="hidden" name="option" value="accesibles">
					<input type="submit" value="Ver museos accesibles" />
					</form></center>"""


BOTON_TODOS = """<center><form method="" action="/">
				<input type="hidden" name="option" value="todos">
				<input type="submit" value="Ver todos los museos" />
				</form></center>"""
				

FORM_DISTRITO = """<center><form action="/museos" method="GET">
    				Distrito:<br>
    				<input type="text" name="distrito" value=""><br>
    				<input type="submit" value="Filtrar">
    				</form></center>"""


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


def get_plantilla(request, titulo, sub_titulo, cont):
	user = request.user
	if request.user.is_authenticated():
		log = "Logged in as " + request.user.username + ".<br><a href\
		='/logout'>Logout</a>"
		try:
			user_name = User.objects.get(username=request.user.username)
			usuario = Usuario.objects.get(nombre=user_name)
			color = usuario.color
			size = usuario.size
		except:  # cuando el usuario existe pero no ha seleccionado nada
			color = ""
			size = ""
	else:
		log = FORM_LOGUEAR
		color = "" 	# tomara el valor por defecto en el css
		size = ""
	
	template = get_template("plantilla/index.html")
	c = Context({'titulo': titulo, 'sub_titulo': sub_titulo, 'cont': cont, 
	'log': log, 'color': color, 'size': size, 'user': user})
	my_template = template.render(c)
	return my_template


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
		html = "VACIO"
		return html

	if total < MAX:
		lista = lista[0:total]
	else:
		lista = lista[0:MAX] # solo los 5 mas seleccionados

	html = ""
	mas = "<i>Más información...</i>"
	num = 0
	for m in museos_DB:
		if m.selecciones in lista and num < MAX:
			num = num + 1
			enlace_name = "<p><b> - <a href='" + m.link + "'>" + m.name + "</a></b></p>"
			html += enlace_name + "<p>" + m.direccion + " <a href\
			='/museos/" + str(m.id) + "'>" + mas + "</a></p>"
	return html


@csrf_exempt		
def root_page(request):
	titulo = "PAGINA PRINCIPAL - MUSEOS DE MADRID"
	sub_titulo = "Museos más seleccionados: "
	if request.method == "GET":
		try:
			option = request.GET['option']
			if option == "accesibles": # MUSEOS ACCESIBLES
				museos_DB = Museo.objects.filter(access="1")
				cont = BOTON_TODOS
				sub_titulo = "Museos más seleccionados y accesibles:"
			else: # TODOS
				museos_DB = Museo.objects.all()
				cont = BOTON_ACCESIBLES

		except MultiValueDictKeyError:  # TODOS LOS MUSEOS
			museos_DB = Museo.objects.all()
			cont = BOTON_ACCESIBLES
	else:  # POST - HAN INICIADO SESION	
		user_name = request.POST['user']
		user_pass = request.POST['pass']
		autent = authenticate(username=user_name, password=user_pass)
		if autent is None:
			error = "ERROR AL INICIAR SESION"
			cont = error
		else:
			login(request, autent)
		return HttpResponseRedirect('/')
		
	# 5 MUSEOS MAS SELECCIONADOS
	museos_mas = mas_seleccionados(museos_DB)
	if museos_mas == "VACIO":
		cont += "<p>No existen museos ACCESIBLES entre los más seleccionados</p>"
	else:
		cont += museos_mas
	
	# PAGINAS PERSONALES DISPONIBLES
	pags_user = "<h2> PÁGINAS PERSONALES DISPONIBLES </h2>"
	lista = []
	users_s = Seleccion.objects.all()
	for u in users_s:
		user_name = u.usuario.nombre
		title = u.usuario.titulo
		if user_name not in lista:
			if title == "":
				title = "Pagina de " + user_name
			pags_user += "<p><b><a href='" + user_name + "'>" + title + "</a></b> |\
			 Usuario: " + user_name + "</p>"
		lista.append(user_name)
	
	cont += pags_user
	my_template = get_plantilla(request, titulo, sub_titulo, cont)
	return HttpResponse(my_template)


def boton_seleccion(ide):
	html = "<form method='POST' action='/museos/'>\
			<input type='hidden' name='id_selecc' value='" + ide + "'>\
			<input type='submit' value='Seleccionar este museo'/>\
			</form>"
	return html


@csrf_exempt
def lista_museos(request):
	ver_mas = "<i>ver más...</i>"
	nuevo_add = ""
	titulo = "MUSEOS DE MADRID:"
	sub_titulo = "Listado general: "

	try: # GET
		distrito = request.GET['distrito']
		sub_titulo = 'Listado de museos para el distrito "' + distrito + '":'
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
			sub_titulo = 'Nuevo museo "' + museo_DB.name + '" añadido!'
		
		try:  # museo ya seleccionado
			Seleccion.objects.get(museo=museo_DB, usuario=usuario)
			sub_titulo = 'Museo "' + museo_DB.name + '" ya añadido anteriormente.'
		except:  # si no lo ha seleccionado antes		
			new_selecc = Seleccion(museo=museo_DB, usuario=usuario)
			new_selecc.save()
			museo_DB.selecciones = museo_DB.selecciones + 1
			museo_DB.save()
			sub_titulo = 'Nuevo museo "' + museo_DB.name + '" añadido!'

	cont = FORM_DISTRITO
	for my_museo in museos_DB:
		cont += ("<li> "+ "<b>" + my_museo.name + "</b><a href='/museos/" + str(my_museo.id) + "'>" 
		+ ", " + ver_mas + "</a>")
		if request.user.is_authenticated():
			cont += boton_seleccion(str(my_museo.id))

	my_template = get_plantilla(request, titulo, sub_titulo, cont)
	return HttpResponse(my_template)


def caja_comentario(ide):
	html = "<form action='/museos/" + ide + "' method='POST'>\
    		<p>Escribe un comentario: </p><p><input type='text' name='comentario'\
    		value=''></p><p><input type='submit' value='Comentar'></p></form>"

	return (html)


@csrf_exempt
def pag_museo(request, ide):
	my_museo = Museo.objects.get(id=int(ide))
	if my_museo.access == "1":
		access = "SI"
	else:
		access = "NO"
	my_museo.access
	titulo = my_museo.name
	sub_titulo = "INFORMACIÓN: "
	cont = "<p>" + my_museo.descrip + "</p><p>ACCESIBLE: " + access + "</p>"
	cont += "<p><a href ='" + my_museo.link + "'>Enlace oficial</a></p>"
	cont += "<p>Direccion: " + my_museo.direccion + " - " + my_museo.barrio
	cont += " - " + my_museo.distrito + "</p><p>Telefono: " + my_museo.telefono
	cont += "</p><p>Email: " + my_museo.email + "</p>"
	
	total_comments = Comentario.objects.filter(museo=my_museo).count()
	if total_comments != 0:
		comentarios = Comentario.objects.filter(museo=my_museo)
		comments = ""
		n = 1
		for a_comment in comentarios:
			comments += "<p>#" + str(n) + " " + a_comment.texto + "</p>"
			n = n + 1
	else:
		comments = "<p>No existen comentarios.</p>"
	
	cont += "<h2>COMENTARIOS: </h2>"
	cont += comments

	if request.user.is_authenticated():  # PUEDE COMENTAR
		form_comentario = caja_comentario(ide)
		cont += form_comentario
		if request.method == "POST":
			texto = request.POST['comentario']
			new_comment = Comentario(texto=texto, museo=my_museo)
			new_comment.save()
			museo_redirect = "/museos/" + str(ide)
			return HttpResponseRedirect(museo_redirect)

	my_template = get_plantilla(request, titulo, sub_titulo, cont)
	return HttpResponse(my_template)


def personalizar(a_user, option):
	name = {'1': 'titulo', '2': 'color', '3':'size'}
	cambio = {'1': 'TITULO PERSONAL', '2': 'COLOR DE FONDO', '3':'TAMAÑO DE LETRA (px)'}
	form = ("<center><form action='/" + a_user + "/' method='POST'>" + cambio[option] + 
			"<input type='text' name='" + name[option] +"' value=''>\
    		<input type='hidden' name='option' value='" + option + "'>\
    		<input type='submit' value='Cambiar'></p>\
    		</form></center>")
	return form


def museos_seleccionados(a_user, pag):
	contenido = ""
	usuario = Usuario.objects.filter(nombre=a_user)
	total_s = Seleccion.objects.filter(usuario=usuario).count()
	if total_s == 0:
		return "NO EXISTEN MUSEOS SELECCIONADOS"
	
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
			enlace_name = "<p> - <a href='" + s.museo.link + "'>" + "<b>" + s.museo.name + "</b>" + "</a></p>"
			contenido += enlace_name + "<p>" + s.museo.direccion
			contenido += "  | " + str(s.date) + "</p>"
		aux = aux + 1

	num_pags = math.ceil(total_s/MAX)  # redondea al entero superior
	numeracion = ""
	for i in range(num_pags):
		numeracion += "<a href='/" + a_user + "=" + str(i+1) + "'>" + str(i+1) + "</a>"
		numeracion += " "
	
	contenido += "<center>" + numeracion + "</center>"
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


def boton_json(a_user):
	form_json = "<center><form method='GET' action='/" + a_user + "/json'>\
				<input type='submit' value='VER CANAL JSON' />\
				</form></center>"
	return form_json


@csrf_exempt	
def pag_usuario(request, a_user):
	try:
		[a_user, pag] = a_user.split('=')
	except ValueError:
		pag = "1"

	if request.method == "GET":
		cont = boton_json(a_user)
		if request.user.is_authenticated():
			try:
				user_logueado = request.user.username
				usuario = Usuario.objects.get(nombre=a_user)
				titulo = generar_titulo(a_user)
				cont += museos_seleccionados(a_user, pag)
				if user_logueado == a_user:
					form_titulo = personalizar(a_user, option="1")
					form_color = personalizar(a_user, option="2")
					form_size = personalizar(a_user, option="3")
					cont += "<h2> PERSONALIZA TU PÁGINA: </h2>"
					cont += form_titulo + form_color + form_size
			except: # si no ha seleccionado nada antes
				# no puede personalizar pagina
				print("Unexpected error:", sys.exc_info()[0])
				titulo = "Pagina de " + a_user
				cont += "No tienes museos seleccionados"
		
		else:  # visitante que entra a la pagina de un usuario
			titulo = generar_titulo(a_user)
			usuario = Usuario.objects.get(nombre=a_user)
			cont += museos_seleccionados(a_user, pag)
		
		sub_titulo = "Museos seleccionados por " + a_user + ":"
		my_template = get_plantilla (request, titulo, sub_titulo, cont)
		return HttpResponse(my_template)
		
	else: # POST
		# solo lo cambian usuarios logueados y que han seleccionado algun museo
		pag_user = "/" + a_user
		usuario = Usuario.objects.get(nombre=a_user)
		opcion = request.POST['option']
		if opcion == '1': # CAMBIAR TITULO
			new_titulo = request.POST['titulo']
			usuario.titulo = new_titulo
		elif opcion == '2':  # CAMBIAR COLOR DE FONDO
			new_color = request.POST['color']
			usuario.color = new_color
		else:  # CAMBIAR TAMAÑO DE LETRA
			new_size = request.POST['size']
			usuario.size = new_size + "px"
		usuario.save()
		return HttpResponseRedirect(pag_user)

	
def canal_usuario(request, a_user):  # canal JSON para los museos seleccionados
	try:
		usuario = Usuario.objects.filter(nombre=a_user)
		seleccionados = Seleccion.objects.filter(usuario=usuario)
		data={}
		for s in seleccionados:
			data[s.museo.name] = {"name": s.museo.name,
					"descrip": s.museo.descrip,
					"access": s.museo.access,
					"direccion": s.museo.direccion,
					"barrio": s.museo.barrio,
					"distrito": s.museo.distrito,
					"telefono": s.museo.telefono,
					"email": s.museo.email
					}
		dump = json.dumps(data)
		return HttpResponse(dump, content_type='application/json')
	except:
		return HttpResponse("Usuario no ha seleccionado ningún museo")


def about(request):
	template = get_template("plantilla/index.html")
	titulo = "Sobre la práctica: "
	sub_titulo = "Información importante: "
	cont = "Autor: Flavio Alonso Arrunátegui Requejo"
	cont += "<p>Grado: Sistemas de Telecomunicaciones</p>"
	cont += "<p> La práctica consiste en una página sobre museos de Madrid donde podrás obtener información básica sobre ellos, comentar los museos, filtrar por distritos, seleccionar los que más te guste a tu página personal siempre y cuando hayas iniciado sesión, visitar su página oficial, etc.</p>"
	cont += "<p>En la página principal (HOME) se mostrarán los museos más seleccionados por los usuarios y las páginas de estos. Se podrán filtrar los museos accesibles entre los más seleccionados.</p>"
	cont += "<p>En la página de museos (MUSEOS) podrás ver todos los museos disponibles, filtrarlos por distrito y seleccionar el museo de tu interés a tu página personal (siempre que estés logueado). Puedes también acceder a la página de cada museo y comentar.</p>"
	cont += "<p>Si estás logueado podrás acceder a tu paǵina personal (MI PERFIL) y ver tus museos seleccionados y la hora en los que los seleccionaste. Aquí podras personalizar la página en general (cambiando el color de fondo o el tamaño de la letra)</p>"
	cont += "<p>La pestaña de CARGAR MUSEOS permite obtener de la página oficial todos los museos y guardarlos en una base de datos. CUIDADO: También elimina todo lo guardado anteriormente en la Base de Datos.</p>"
	my_template = get_plantilla(request, titulo, sub_titulo, cont)
	return HttpResponse(my_template)
