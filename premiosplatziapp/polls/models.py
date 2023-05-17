import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
#aca creo la tabla de Questions
class Question(models.Model):
    question_text = models.CharField(max_length=200) #models ya trae esta forma de definir que tipo de dato es, charfield es para varchar
    pub_date = models.DateTimeField('date tublished') #con datetime es mas facil, solo se da el nombre al que hace referencia('cualquier cosa') 
    
    #defino un metodo dentro de la clase
    #con esto digo que cada vez que invoco a un objeto del tipo Question en la consola o codigo, lo que queremos que django nos muestre es el question_text
    #por ende que nos muestre el valor de texto en si, y no  <QuerySet [<Question: Question object (1)>]>
    def __str__(self):
        return self.question_text
    
    
    #esto retorna verdadero o falso si la pregunta fue publicada recientemente
    def was_published_recently(self):
        #con esto tomo el dia actual y con datetime le resto 1 dia
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1) #timedelta nos define una diferencia de tiempo

#y aca la tabla de choices
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)#aca lo conecto a Questions(foreign key), CASCADE hace que si yo borro una pregunta se borre en cascada las otras preguntas
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)#va a ser un contador que va desde 0 y va acumulando 
    
    def __str__(self):
        return self.choice_text