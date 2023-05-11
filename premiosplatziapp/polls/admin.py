from django.contrib import admin
from .models import Question, Choice #importo Question (el . es para decir que estoy en la misma carpeta)

# Register your models here.
admin.site.register([Question,Choice]) #y hago mi modelo de datos disponible en /admin