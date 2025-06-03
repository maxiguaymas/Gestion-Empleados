from django.urls import path
from . import views

urlpatterns = [
    path('cargar/', views.cargar_recibo, name='cargar_recibo'),
    path('ver/', views.ver_recibos, name='ver_recibos'),
]