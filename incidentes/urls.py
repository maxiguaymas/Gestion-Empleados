from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_incidente, name='registrar_incidente'),
    path('ver/', views.ver_incidentes, name='ver_incidentes'),
    path('detalle/<int:incidente_id>/', views.detalle_incidente, name='detalle_incidente'),
    # URL para ver los incidentes de un empleado específico
    path('empleado/<int:empleado_id>/', views.ver_incidentes_empleado, name='mis_incidentes'),
]