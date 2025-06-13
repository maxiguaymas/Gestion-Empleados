from django.urls import path
from . import views

urlpatterns = [
    path('cargar/', views.cargar_horario, name='cargar_horario'),
    path('asignar/', views.asignar_horario, name='asignar_horario'),
]