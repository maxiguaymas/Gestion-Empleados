from django.urls import path
from . import views

urlpatterns = [
    path('cargar/', views.cargar_horario, name='cargar_horario'),
    path('asignar/', views.asignar_horario, name='asignar_horario'),
    path('ver/', views.ver_horarios_asig, name='ver_horarios_asig'),
    path('ver/<int:id>/', views.mis_horarios, name='mis_horarios'),
]