#este es el archivo que nos da django para crear las vistas

from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404 #no confundir, es con object
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question,Choice
from django.urls import reverse
from django.views import generic

'''
# Create your views here.
def index (request):
    latest_question_list = Question.objects.all()
    return render(request, 'polls/index.html', {
        'latest_question_list': latest_question_list
    })


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html",{
        "question": question
    } )


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html",{
        "question": question
    })
'''

#todo lo de arriba lo voy a hacer con una class base view
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        """return the last five published questions"""
        return Question.objects.order_by("-pub_date")[:5] #cuando le pongo el - adelante lo hace en order desc

#reemplazo de detail de arriba    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    
    
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    

def vote(request, question_id):
    question = get_object_or_404(Question, pk= question_id)
    try:
        #por medio de un diccionario del metodo request.POST[] se puede acceder a los datos que se enviaron por el metodo http
        #con POST["choice"] accedo al input que cree en detail.html en input<name="choice">
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        
        #si da un error tira un msj que dice no elegiste la respuesta
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html",{
            "question":question,
            "error_message":"no elegiste una respuesta"
        })
    else:
        #si todo se cumple, el programa va a sumar un voto y lo va a guardar en la base
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,))) #redirect se asegura que el usuario no envie la info dos veces
