from django.contrib import admin

# Register your models here.

from .models import Museo
admin.site.register(Museo)

from .models import Comentario
admin.site.register(Comentario)

from .models import Usuario
admin.site.register(Usuario)

from .models import Seleccion
admin.site.register(Seleccion)
