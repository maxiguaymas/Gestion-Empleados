from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.index, name='index'),
    # path('empleados/', views.empleados, name='empleados'),
    path('empleados/crear/', views.crear_empleado, name='crear_empleado'),
    path('empleados/editar/<int:id>/', views.editar_empleado, name='editar_empleado'),
    path('empleados/eliminar/<int:id>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('empleados/ver/', views.ver_empleados, name='ver_empleados'),
]