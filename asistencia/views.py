import base64
import numpy as np
import cv2
import face_recognition
from datetime import date

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from empleados.models import Empleado
from .models import Rostro, Asistencia


@login_required
def vista_registrar_rostro(request):
    """
    Renderiza la página para registrar el rostro de un empleado.
    Pasa a la plantilla los empleados que aún no tienen un rostro registrado.
    """
    empleados_registrados_ids = Rostro.objects.values_list('id_empl_id', flat=True)
    empleados_sin_rostro = Empleado.objects.exclude(id__in=empleados_registrados_ids)
    context = {
        'empleados': empleados_sin_rostro
    }
    return render(request, 'registrar_rostro.html', context)


@login_required
def api_guardar_rostro(request):
    """
    API para recibir una imagen, extraer el encoding facial y guardarlo.
    """
    if request.method == 'POST':
        empleado_id = request.POST.get('empleado_id')
        image_data = request.POST.get('image') # Imagen en formato base64

        if not empleado_id or not image_data:
            return JsonResponse({'status': 'error', 'message': 'Faltan datos.'}, status=400)

        try:
            # Decodificar la imagen
            format, imgstr = image_data.split(';base64,') 
            ext = format.split('/')[-1] 
            data = base64.b64decode(imgstr)
            
            # Convertir a imagen de OpenCV
            nparr = np.frombuffer(data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Encontrar rostros y calcular encoding
            face_locations = face_recognition.face_locations(rgb_img)
            if len(face_locations) != 1:
                return JsonResponse({'status': 'error', 'message': f'Se detectaron {len(face_locations)} rostros. Se necesita exactamente uno.'})

            face_encodings = face_recognition.face_encodings(rgb_img, face_locations)
            
            # Guardar en la base de datos
            empleado = Empleado.objects.get(id=empleado_id)
            rostro, created = Rostro.objects.get_or_create(id_empl=empleado)
            rostro.set_encoding(face_encodings[0])
            rostro.save()

            return JsonResponse({'status': 'success', 'message': f'Rostro de {empleado.nombre} registrado exitosamente.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)


@login_required
def vista_marcar_asistencia(request):
    """Renderiza la página para marcar asistencia con la cámara."""
    return render(request, 'marcar_asistencia.html')


@login_required
def api_reconocer_rostro(request):
    """
    API para recibir un frame de la cámara, reconocer el rostro y registrar la asistencia.
    """
    if request.method == 'POST':
        image_data = request.POST.get('image')
        if not image_data:
            return JsonResponse({'status': 'error', 'message': 'No se recibió imagen.'}, status=400)

        # Cargar encodings conocidos
        rostros_conocidos = Rostro.objects.all()
        encodings_conocidos = [np.array(r.get_encoding()) for r in rostros_conocidos]
        empleados_ids = [r.id_empl_id for r in rostros_conocidos]

        # Decodificar imagen recibida
        format, imgstr = image_data.split(';base64,')
        data = base64.b64decode(imgstr)
        nparr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Buscar rostros y comparar
        face_locations = face_recognition.face_locations(rgb_img)
        face_encodings = face_recognition.face_encodings(rgb_img, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(encodings_conocidos, face_encoding, tolerance=0.5)
            if True in matches:
                first_match_index = matches.index(True)
                empleado_id = empleados_ids[first_match_index]
                empleado = Empleado.objects.get(id=empleado_id)
                
                # Registrar asistencia (solo una vez por día)
                if not Asistencia.objects.filter(id_empl=empleado, fecha_hora__date=date.today()).exists():
                    Asistencia.objects.create(id_empl=empleado)                
                    return JsonResponse({'status': 'success', 'nombre': f'{empleado.nombre} {empleado.apellido}'})                
                else:
                    return JsonResponse({'status': 'already_marked', 'nombre': f'{empleado.nombre} {empleado.apellido}'})

        return JsonResponse({'status': 'not_found'})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)

@login_required
def ver_asistencias_empleado(request, empleado_id):
    """
    Muestra una lista de todas las asistencias para un empleado específico,
    ordenadas de la más reciente a la más antigua.
    """
    empleado = get_object_or_404(Empleado, id=empleado_id)
    asistencias = Asistencia.objects.filter(id_empl=empleado).order_by('-fecha_hora')
    
    context = {
        'empleado': empleado,
        'asistencias': asistencias
    }
    return render(request, 'ver_asistencias.html', context)