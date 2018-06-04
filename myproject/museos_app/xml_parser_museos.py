#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.sax.handler import ContentHandler
import sys
from .models import Museo
from xml.sax import make_parser


def normalize_whitespace(text):
	return string.join(string.split(text), ' ')


class myContentHandler(ContentHandler):
	def __init__ (self):
		self.atributo = ""
		self.inContent = False
		self.theContent = ""
		self.name = ""
		self.descripcion = ""
		self.accesibilidad = ""
		self.link = ""
		self.direccion = ""
		self.barrio = ""
		self.distrito = ""
		self.telefono = ""
		self.email = ""


	def startElement (self, name, attrs):
		if name == 'atributo':
			self.atributo = attrs.get('nombre')
		if self.atributo in ['NOMBRE', 'DESCRIPCION-ENTIDAD',
							'ACCESIBILIDAD', 'CONTENT-URL', 'NOMBRE-VIA',
							'CLASE-VIAL', 'NUM', 'BARRIO', 'DISTRITO', 
							'TELEFONO', 'EMAIL']:
			self.inContent = True

            
	def endElement (self, name):
		if self.atributo == 'NOMBRE':
			self.name = self.theContent
		elif self.atributo == 'DESCRIPCION-ENTIDAD':
			self.descripcion = self.theContent			
		elif self.atributo == 'ACCESIBILIDAD':
			self.accesibilidad = self.theContent
		elif self.atributo == 'CONTENT-URL':
			self.link = self.theContent
		elif self.atributo == 'NOMBRE-VIA':  # direccion
			global via
			via = self.theContent
		elif self.atributo == 'CLASE-VIAL':
			self.direccion = self.theContent
		elif self.atributo == 'NUM':
			self.direccion = self.direccion + " " + via + ", " + self.theContent
			print(self.direccion)
		elif self.atributo == 'BARRIO':
			self.barrio = self.theContent
		elif self.atributo == 'DISTRITO':
			self.distrito = self.theContent	
		elif self.atributo == 'TELEFONO':
			self.telefono = self.theContent	
		elif self.atributo == 'EMAIL':
			self.email = self.theContent
		
		self.inContent = False
		self.theContent = ""	
		self.atributo = ""
		
		if name == 'contenido':
			museo = Museo(name = self.name, descrip = self.descripcion, 
			access = self.accesibilidad, link = self.link, 
			direccion = self.direccion, barrio = self.barrio, 
			distrito = self.distrito, telefono = self.telefono, email = self.email)
			
			museo.save()

			self.inContent = False
			self.theContent = ""		
			self.atributo = ""  # inicializamos nuevamente
			self.name = ""
			self.descripcion = ""
			self.accesibilidad = ""
			self.link = ""
			self.direccion = ""
			self.barrio = ""
			self.distrito = ""
			self.telefono = ""
			self.email = ""
			
								
	def characters (self, chars):
		if self.inContent:
			self.theContent = self.theContent + chars

def parsear():
	# Load parser and driver
	theParser = make_parser()
	theHandler = myContentHandler()
	theParser.setContentHandler(theHandler)
	# Ready, set, go!
	theParser.parse("https://datos.madrid.es/egob/catalogo/201132-0-museos.xml")
