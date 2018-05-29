from django.db import models

# Create your models here.

class Museo(models.Model):
	identidad = models.CharField(max_length=10)
	name = models.CharField(max_length=128)
	descrip = models.TextField()
	access = models.CharField(max_length=1)  # accesible 'O' o '1'
	link = models.CharField(max_length=512)
	direccion = models.TextField()
	barrio = models.CharField(max_length=128)
	distrito = models.CharField(max_length=128)
	telefono = models.CharField(max_length=9)
	email = models.CharField(max_length=128)
	
	num_selecciones = models.IntegerField(default=0)
	def __str__(self):
		return self.name


class Comentario(models.Model):
	texto = models.TextField()
	museo = models.ForeignKey(Museo)
