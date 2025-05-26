from django.shortcuts import render
from django.shortcuts import redirect
from .forms import EmpleadoForm
from .models import Empleado

# Create your views here.
def index(request):
    return render(request, 'index.html')

def crear_empleado(request):
    form = EmpleadoForm()

    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, 'crear_empleado.html', {'form': form, 'error': 'Por favor corrige los errores.'})

    return render(request, 'crear_empleado.html', {'form': form})

def editar_empleado(request, id):
    try:
        empleado = Empleado.objects.get(id=id)
    except Empleado.DoesNotExist:
        return redirect('index')
    form = EmpleadoForm(instance=empleado)

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, 'editar_empleado.html', {'form': form, 'error': 'Por favor corrige los errores.'})

    return render(request, 'editar_empleado.html', {'form': form})

def eliminar_empleado(request, id):
    empleado = Empleado.objects.get(id=id)
    
    if request.method == 'POST':
        empleado.delete()
        return redirect('index')
    
    return render(request, 'eliminar_empleado.html', {'empleado': empleado})

def ver_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleados.html', {'empleados': empleados})
    