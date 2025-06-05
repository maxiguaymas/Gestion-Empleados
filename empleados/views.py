from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import EmpleadoForm
from .models import Empleado

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def crear_empleado(request):
    form = EmpleadoForm()

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, 'crear_empleado.html', {'form': form, 'error': 'Por favor corrige los errores.'})

    return render(request, 'crear_empleado.html', {'form': form})

@login_required
def editar_empleado(request, id):
    try:
        empleado = Empleado.objects.get(id=id)
    except Empleado.DoesNotExist:
        return redirect('index')
    form = EmpleadoForm(instance=empleado)

    if request.method == 'POST':
        form = EmpleadoForm(request.POST,request.FILES, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, 'editar_empleado.html', {'form': form, 'error': 'Por favor corrige los errores.'})

    return render(request, 'editar_empleado.html', {'form': form})

@login_required
def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    empleado.fecha_egreso = timezone.now().date()
    empleado.estado = 'Inactivo'
    empleado.save()
    return redirect('ver_empleados')

@login_required
def ver_empleados(request):
    empleados = Empleado.objects.filter(fecha_egreso__isnull=True)
    return render(request, 'empleados.html', {'empleados': empleados})

@login_required
def ver_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    return render(request, 'ver_empleado.html', {'empleado': empleado})
    