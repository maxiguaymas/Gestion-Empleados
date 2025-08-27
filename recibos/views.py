from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from empleados.models import Recibo_Sueldos as Recibo, Empleado
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
def ver_recibos(request):
    """
    Vista para que un administrador vea y filtre recibos de sueldo.
    Filtra por empleado si se pasa un 'id' en los parámetros GET.
    """
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para ver los recibos.")
        return redirect('login')

    # Empezamos con una consulta vacía. Los recibos solo se mostrarán después de una búsqueda.
    recibos = Recibo.objects.none()
    mensaje = None
    empleado_seleccionado = None

    empleado_id = request.GET.get('id')

    if empleado_id:
        try:
            empleado_seleccionado = Empleado.objects.get(id=int(empleado_id))
            recibos = Recibo.objects.filter(id_empl=empleado_seleccionado).order_by('-fecha_emision')
            if not recibos.exists():
                mensaje = f"No se encontraron recibos para {empleado_seleccionado.nombre} {empleado_seleccionado.apellido}."
        except (ValueError, Empleado.DoesNotExist):
            mensaje = "El empleado seleccionado no es válido o no fue encontrado."
    else:
        mensaje = "Por favor, busque un empleado para ver sus recibos."

    return render(request, 'ver_recibos.html', {
        'recibos': recibos,
        'mensaje': mensaje,
        'empleado_seleccionado': empleado_seleccionado,
    })
    
def mis_recibos(request):
    try:
        # Asume que el modelo User tiene una relación con Empleado (ej. OneToOneField 'empleado').
        # Si la relación tiene otro nombre, ajústalo aquí.
        empleado = request.user.empleado
        recibos = Recibo.objects.filter(id_empl=empleado).order_by('-fecha_emision')
        mensaje = "Aún no tienes recibos de sueldo registrados." if not recibos.exists() else None
    except AttributeError:
        # Esto ocurre si el usuario logueado no es un empleado (ej. es un superuser sin perfil de empleado)
        recibos = Recibo.objects.none()
        mensaje = "Tu usuario no está asociado a un perfil de empleado."
        empleado = None
    return render(request, 'mis_recibos.html', {
        'recibos': recibos,
        'mensaje': mensaje,
        'empleado_seleccionado': empleado,
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
