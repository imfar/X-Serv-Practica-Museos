"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
from django.contrib.auth.views import logout, login

urlpatterns = [
	url(r'^$', 'museos_app.views.root_page'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^plantilla/(.*)', serve, {'document_root': 'templates/plantilla'}),
    url(r'about/$', 'museos_app.views.about'),
    url(r'^update$', 'museos_app.views.update'),
    url(r'^museos/$', 'museos_app.views.lista_museos'),
    url(r'^museos/(.+)$', 'museos_app.views.pag_museo'),
    url(r'^logout', 'museos_app.views.logout_view'),
    url(r'^(.+)/json$', 'museos_app.views.canal_usuario'),
    url(r'^(.+)/$', 'museos_app.views.pag_usuario'),
]
