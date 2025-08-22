from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from empleados.models import Recibo_Sueldos, Empleado
from .forms import ReciboSueldoForm  # Debes crear este formulario
from empleados.views import es_admin
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(es_admin)
def cargar_recibo(request):
    # Solo permitir acceso a usuarios logeados
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para cargar un recibo.")
        return redirect('login')
    
    if request.method == 'POST':
        form = ReciboSueldoForm(request.POST, request.FILES)
        empleado_id = request.POST.get('id_empl')
        if empleado_id:
            form.fields['id_empl'].queryset = Empleado.objects.filter(id=empleado_id)
        if form.is_valid():
            form.save()
            messages.success(request, "Recibo cargado correctamente.")
            return redirect('ver_recibos')
    else:
        form = ReciboSueldoForm()
        form.fields['id_empl'].queryset = Empleado.objects.none()
    return render(request, 'cargar_recibo.html', {'form': form})

@user_passes_test(es_admin)
def ver_recibos(request, id=None):
    # Solo permitir acceso a usuarios logeados
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para ver los recibos.")
        return redirect('login')
    recibos = []
    mensaje = None

    if id is not None:
        # Vista para /recibos/ver/<id>/
        try:
            empleado = Empleado.objects.get(id=int(id))
            recibos = Recibo_Sueldos.objects.filter(id_empl=empleado)
            if not recibos:
                mensaje = "No hay recibos para este empleado."
        except Empleado.DoesNotExist:
            mensaje = "No se encontró un empleado con ese ID."
        return render(request, 'mis_recibos.html', {
            'recibos': recibos,
            'mensaje': mensaje,
        })
    else:
        # Vista para /recibos/ver/
        id_query = request.GET.get('id')
        if id_query:
            try:
                empleado = Empleado.objects.get(id=int(id_query))
                recibos = Recibo_Sueldos.objects.filter(id_empl=empleado)
                if not recibos:
                    mensaje = "No hay recibos para este empleado."
            except Empleado.DoesNotExist:
                mensaje = "No se encontró un empleado con ese DNI."
        return render(request, 'ver_recibos.html', {
            'recibos': recibos,
            'mensaje': mensaje,
            'dni': id_query,
        })

def ajax_buscar_empleado(request):
    q = request.GET.get('q', '')
    empleados = Empleado.objects.filter(dni__icontains=q)[:10]
    results = []
    for emp in empleados:
        results.append({
            'id': emp.id,
            'text': f"{emp.dni} - {emp.nombre} {emp.apellido}"
        })
    return JsonResponse({'results': results})


