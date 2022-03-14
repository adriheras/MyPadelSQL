
from django.contrib import admin
from django.urls import  path
from principal import views

urlpatterns = [  
    path('', views.inicio),
    path('busca_jugadores_nombre/', views.busca_jugadores_nombre),
    path('lista_jugadores_posicion/', views.lista_jugadores_posicion),
    path('cargar/', views.cargar),
    path('estadisticas/', views.estadisticas),
    path('busca_jugadores_ciudad/', views.busca_jugadores_ciudad),
    path('filtra_jugadores_edad/', views.filtra_jugadores_edad),
    path('ranking/', views.lista_jugadores),
    path('admin/', admin.site.urls),
]
