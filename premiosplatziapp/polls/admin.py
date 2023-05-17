from django.contrib import admin
from .models import Question, Choice #importo Question (el . es para decir que estoy en la misma carpeta)

class ChoiceInline(admin.StackedInline):
    model = Choice
    #cantidad de respuesta que quiero por cada choice
    extra = 3

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]
    #adjunto el inline de arriba
    inlines = [ChoiceInline]
    #edito como se ve la lista del modelo que estamos editando en admin, le agrego la fecha de creacion y si fue creado recientemente
    list_display = ("question_text", "pub_date", "was_published_recently")
    #agrego filtros
    list_filter = ["pub_date"]
    #busqueda por medio de palabras de las question
    search_fields = ["question"]

admin.site.register(Question, QuestionAdmin) #y hago mi modelo de datos disponible en /admin