from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.contrib import messages
from empleados.views import es_admin
from django.core.exceptions import PermissionDenied
from empleados.models import Incidente, IncidenteEmpleadoDescargo, Empleado, SancionEmpleado
from .forms import IncidenteForm
from sanciones.forms import SancionMasivaForm

@login_required
@user_passes_test(es_admin)
@transaction.atomic # Para asegurar la integridad de los datos
def registrar_incidente(request):
    if request.method == 'POST':
        form = IncidenteForm(request.POST)
        if form.is_valid():
            # Primero, guardamos el incidente principal
            incidente = form.save()

            # Obtenemos los datos adicionales del formulario
            empleados = form.cleaned_data['empleados_involucrados']
            observaciones = form.cleaned_data['observaciones']
            responsable = request.user.get_full_name() or request.user.username

            # Ahora, creamos un registro en IncidenteEmpleadoDescargo para cada empleado
            for empleado in empleados:
                IncidenteEmpleadoDescargo.objects.create(
                    id_incidente=incidente,
                    id_empl=empleado,
                    fecha_ocurrencia=incidente.fecha_incid,
                    observaciones=observaciones,
                    responsable_registro=responsable,
                    estado=True # O el estado inicial que definas
                )
            
            messages.success(request, 'El incidente ha sido registrado exitosamente.')
            # Redirigir a una futura vista de lista de incidentes
            return redirect('ver_incidentes') # Asumimos que esta ruta existirá

    else:
        form = IncidenteForm()

    return render(request, 'registrar_incidente.html', {'form': form})

# También necesitarás una vista para listar los incidentes
@login_required
@user_passes_test(es_admin)
def ver_incidentes(request):
    incidentes = Incidente.objects.all().order_by('-fecha_incid')
    return render(request, 'ver_incidentes.html', {'incidentes': incidentes})

@login_required
@user_passes_test(es_admin)
def detalle_incidente(request, incidente_id):
    incidente = get_object_or_404(Incidente, id=incidente_id)
    
    # Obtenemos los involucrados y verificamos si ya tienen una sanción para este incidente
    involucrados_qs = IncidenteEmpleadoDescargo.objects.filter(id_incidente=incidente).select_related('id_empl')
    sanciones_existentes = SancionEmpleado.objects.filter(incidente_asociado__in=involucrados_qs).values_list('incidente_asociado_id', flat=True)

    involucrados = []
    for inv in involucrados_qs:
        inv.ya_sancionado = inv.id in sanciones_existentes
        involucrados.append(inv)

    # Pre-llenamos el motivo del formulario de sanción
    motivo_inicial = f"Derivado del incidente: '{incidente.nombre_incid}' ocurrido el {incidente.fecha_incid.strftime('%d/%m/%Y')}."
    sancion_form = SancionMasivaForm(initial={'motivo': motivo_inicial})
    
    return render(request, 'detalle_incidente.html', {
        'incidente': incidente,
        'involucrados': involucrados,
        'sancion_form': sancion_form
    })

@login_required
def ver_incidentes_empleado(request, empleado_id):
    # Obtenemos el empleado o mostramos un error 404 si no existe
    empleado = get_object_or_404(Empleado, id=empleado_id)
    # Lógica de permisos:
    # Permitir si es admin O si el empleado está editando su propio perfil.
    es_propietario = hasattr(request.user, 'empleado') and request.user.empleado.id == empleado.id
    if not (es_admin(request.user) or es_propietario):
        raise PermissionDenied

    # Buscamos todas las entradas en IncidenteEmpleadoDescargo para este empleado.
    # Usamos select_related para optimizar la consulta y traer los datos del incidente relacionado
    # en una sola query a la base de datos.
    incidentes_empleado = IncidenteEmpleadoDescargo.objects.filter(id_empl=empleado).select_related('id_incidente').order_by('-fecha_ocurrencia')

    context = {
        'empleado': empleado,
        'incidentes_empleado': incidentes_empleado
    }

    return render(request, 'ver_incidentes_empleado.html', context)