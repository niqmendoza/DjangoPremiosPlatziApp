from django.urls import path

#tengo que importar views para que la aplicacion me cargue las function base views
from . import views #cuando pongo . es para referir a esta misma carpeta de polls

app_name="polls"

#dentro de urlpatterns van a estar todas las urls que va a usar urls.py del proyecto principal(premiosplatziapp)
urlpatterns = [
    #accedo con /polls/
    path('', views.IndexView.as_view(), name='index'),
    
    #'<int:questio_id>/' es la forma que django nos da para pasar parametros variables mediante la url que usamos para una pagina web
    #accedo con /polls/5/
    path('<int:pk>/detail/', views.DetailView.as_view(), name='detail'), 
    
    #accedo con /polls/5/results
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    
    #accedo con /polls/5/votes
    path('<int:pk>/vote/', views.vote, name='vote'),
]
