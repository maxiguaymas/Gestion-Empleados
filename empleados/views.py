from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import EmpleadoForm
from .models import Empleado
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

def es_admin(user):
    return user.groups.filter(name='Administrador').exists() or user.is_superuser
# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
@user_passes_test(es_admin)
def crear_empleado(request):
    form = EmpleadoForm()

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            empleado = form.save(commit=False)
            dni = form.cleaned_data['dni']
            grupo = form.cleaned_data['grupo']
            user = User.objects.create_user(username=str(dni), password=str(dni))
            user.groups.add(grupo)
            user.save()
            empleado.user = user
            empleado.save()
            return redirect('ver_empleados')
        else:
            return render(request, 'crear_empleado.html', {'form': form, 'error': 'Por favor corrige los errores.'})

    return render(request, 'crear_empleado.html', {'form': form})

@login_required
@user_passes_test(es_admin)
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
@user_passes_test(es_admin)
def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    empleado.fecha_egreso = timezone.now().date()
    empleado.estado = 'Inactivo'
    empleado.save()
    return redirect('ver_empleados')

@login_required
@user_passes_test(es_admin)
def ver_empleados(request):
    empleados = Empleado.objects.filter(fecha_egreso__isnull=True)
    return render(request, 'empleados.html', {'empleados': empleados})

@login_required
@user_passes_test(es_admin)
def ver_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    return render(request, 'ver_empleado.html', {'empleado': empleado})
    