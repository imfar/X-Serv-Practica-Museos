from django.db import models
from django.utils import timezone

# Create your models here.

class Museo(models.Model):
	identidad = models.CharField(max_length=10)
	name = models.CharField(max_length=128)
	descrip = models.TextField(default="")
	access = models.CharField(max_length=1)  # accesible 'O' o '1'
	link = models.CharField(max_length=512)
	direccion = models.TextField()
	barrio = models.CharField(max_length=128)
	distrito = models.CharField(max_length=128)
	telefono = models.CharField(max_length=128)
	email = models.CharField(max_length=128)
	
	selecciones = models.IntegerField(default=0)
	def __str__(self):
		return self.name


class Comentario(models.Model):
	texto = models.TextField()
	museo = models.ForeignKey(Museo)
	def __str__(self):
		return self.museo.name + " , comentarios: " + self.texto


class Usuario(models.Model):
	nombre = models.CharField(max_length=128, default="")
	titulo = models.CharField(max_length=128, default="")
	size = models.CharField(max_length=64, default="")
	color = models.CharField(max_length=64, default="")
	def __str__(self):
		return self.nombre + " " + self.titulo

class Seleccion(models.Model):
	museo = models.ForeignKey(Museo)
	usuario = models.ForeignKey(Usuario)
	date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.museo.name + " - " + self.usuario.nombre + ", " + str(self.date)
