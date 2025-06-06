from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.index, name='index'),
    # path('empleados/', views.empleados, name='empleados'),
    path('crear/', views.crear_empleado, name='crear_empleado'),
    path('editar/<int:id>/', views.editar_empleado, name='editar_empleado'),
    path('eliminar/<int:id>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('ver/', views.ver_empleados, name='ver_empleados'),
    path('ver/<int:id>/', views.ver_empleado, name='ver_empleado'),
]