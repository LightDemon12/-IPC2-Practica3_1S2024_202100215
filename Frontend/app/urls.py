from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('ayuda', views.ayuda, name='ayuda'),
    path('Carga', views.Carga, name='Carga'),
    path('revision', views.revisión, name='Revision'),
    path('cargarXML/', views.cargarXML, name='cargarXML'),
    path('clear/', views.clear_animals, name='clear_animals'),
    path('posts', views.posts, name='posts'),
    path('download', views.download, name='download_file'),
]
