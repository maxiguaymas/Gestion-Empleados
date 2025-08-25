from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import EmpleadoForm
from .models import Empleado
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from empleados.models import Legajo, Documento, RequisitoDocumento

# Agrega estas importaciones
import pandas as pd
import plotly.express as px
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse

def es_admin(user):
    return user.groups.filter(name='Administrador').exists() or user.is_superuser
# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
@user_passes_test(es_admin)
@login_required
@user_passes_test(es_admin)
def crear_empleado(request):
    form = EmpleadoForm()
    requisitos = RequisitoDocumento.objects.all()
    error = None

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES)
        archivos = request.FILES
        # 1. Validar documentos obligatorios
        for req in requisitos:
            if req.obligatorio and not archivos.get(f'doc_{req.id}'):
                error = f"El documento '{req.nombre_doc}' es obligatorio."
                break

        if not error and form.is_valid():
            # 2. Crear usuario, empleado, legajo y documentos
            empleado = form.save(commit=False)
            dni = form.cleaned_data['dni']
            grupo = form.cleaned_data['grupo']
            user = User.objects.create_user(username=str(dni), password=str(dni))
            user.groups.add(grupo)
            user.save()
            empleado.user = user
            empleado.save()

            nro_leg = Legajo.objects.count() + 1
            legajo = Legajo.objects.create(
                id_empl=empleado,
                estado_leg='Activo',
                nro_leg=nro_leg
            )

            for req in requisitos:
                archivo = archivos.get(f'doc_{req.id}')
                Documento.objects.create(
                    id_leg=legajo,
                    id_requisito=req,
                    ruta_archivo=archivo if archivo else None,
                    estado_doc=bool(archivo)
                )
            return redirect('ver_empleados')
        else:
            return render(request, 'crear_empleado.html', {'form': form, 'error': error or 'Por favor corrige los errores.', 'requisitos': requisitos})

    return render(request, 'crear_empleado.html', {'form': form, 'requisitos': requisitos})


@login_required
@user_passes_test(es_admin)
def editar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    legajo = getattr(empleado, 'legajo', None)
    documentos = Documento.objects.filter(id_leg=legajo) if legajo else []
    requisitos = RequisitoDocumento.objects.all()
    error = None

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES, instance=empleado)
        archivos = request.FILES
        if form.is_valid():
            form.save()
            # Actualizar documentos si se suben nuevos archivos
            for req in requisitos:
                archivo = archivos.get(f'doc_{req.id}')
                if archivo and legajo:
                    doc = Documento.objects.filter(id_leg=legajo, id_requisito=req).first()
                    if doc:
                        doc.ruta_archivo = archivo
                        doc.estado_doc = True
                        doc.save()
            return redirect('ver_empleados')
        else:
            return render(request, 'editar_empleado.html', {
                'form': form,
                'error': 'Por favor corrige los errores.',
                'documentos': documentos,
                'requisitos': requisitos,
                'legajo': legajo,
            })

    else:
        form = EmpleadoForm(instance=empleado)

    return render(request, 'editar_empleado.html', {
        'form': form,
        'documentos': documentos,
        'requisitos': requisitos,
        'legajo': legajo,
    })

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
def ver_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    # Lógica de permisos:
    # Permitir si es admin O si el empleado está editando su propio perfil.
    es_propietario = hasattr(request.user, 'empleado') and request.user.empleado.id == empleado.id
    if not (es_admin(request.user) or es_propietario):
        raise PermissionDenied("No tienes permiso para ver este perfil.")
    legajo = getattr(empleado, 'legajo', None)
    documentos = Documento.objects.filter(id_leg=legajo) if legajo else []
    return render(request, 'ver_empleado.html', {
        'empleado': empleado,
        'legajo': legajo,
        'documentos': documentos,
    })

# --- Gráfico de barras empleados activos/inactivos ---
@login_required
@user_passes_test(es_admin)
def grafico_empleados_activos_inactivos(request):
    empleados = Empleado.objects.values('estado')
    df = pd.DataFrame(list(empleados))
    conteo = df['estado'].value_counts().reset_index()
    conteo.columns = ['Estado', 'Cantidad']
    fig = px.bar(conteo, x='Estado', y='Cantidad', title='Empleados Activos vs Inactivos', text='Cantidad')
    fig.update_traces(textposition='outside')
    grafico_html = fig.to_html(full_html=False)
    return render(request, 'grafico_empleados.html', {'grafico': grafico_html})

# --- Exportar gráfico a PDF ---
@login_required
@user_passes_test(es_admin)
def grafico_empleados_pdf(request):
    empleados = Empleado.objects.values('estado')
    df = pd.DataFrame(list(empleados))
    conteo = df['estado'].value_counts().reset_index()
    conteo.columns = ['Estado', 'Cantidad']
    fig = px.bar(conteo, x='Estado', y='Cantidad', title='Empleados Activos vs Inactivos', text='Cantidad')
    fig.update_traces(textposition='outside')
    grafico_html = fig.to_html(full_html=False)

    template = get_template('grafico_empleados_pdf.html')
    html = template.render({'grafico': grafico_html})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="grafico_empleados.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status=500)
    return response
