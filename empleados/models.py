from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import time

# Create your models here.
def validar_mayor_18(value):
    hoy = timezone.now().date()
    edad = hoy.year - value.year - ((hoy.month, hoy.day) < (value.month, value.day))
    if edad < 18:
        raise ValidationError('El empleado debe ser mayor de 18 años.')

class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empleado')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.IntegerField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], default='O')
    estado_civil = models.CharField(max_length=20, choices=[('Soltero', 'Soltero'), ('Casado', 'Casado'), ('Divorciado', 'Divorciado'), ('Viudo', 'Viudo')], default='Soltero')
    fecha_nacimiento = models.DateField(validators=[validar_mayor_18])
    estado = models.CharField(max_length=20, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo'), ('Suspendido', 'Suspendido'), ('Licencia', 'Licencia')], default='Activo')
    ruta_foto = models.ImageField(upload_to='empleados/fotos/', blank=True, null=True)
    fecha_ingreso = models.DateField(auto_now_add=True)
    fecha_egreso = models.DateField(blank=True, null=True)
    


    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.dni}"
    

   # Clase Recibo_Sueldos debe estar al mismo nivel que Empleado
class Recibo_Sueldos(models.Model):
    id_empl = models.ForeignKey('Empleado', on_delete=models.CASCADE, related_name='recibos')
    fecha_emision = models.DateField()
    periodo = models.CharField(max_length=7)
    ruta_pdf = models.FileField(upload_to='recibos/pdf/')
    ruta_imagen = models.ImageField(upload_to='recibos/imagenes/', blank=True, null=True)

    def __str__(self):
        return f"Recibo {self.id_recibo} - {self.id_empl.nombre} {self.id_empl.apellido}"
  #Clase horarios debe estar al mismo nivel que Empleado
class Horarios(models.Model):
    turno = models.CharField(max_length=20, choices=[('Mañana', 'Mañana'), ('Tarde', 'Tarde')], default='Mañana')
    dia = models.CharField(max_length=10, choices=[('Lunes', 'Lunes'), ('Martes', 'Martes'), ('Miércoles', 'Miércoles'), ('Jueves', 'Jueves'), ('Viernes', 'Viernes')])
    HORA_ENTRADA_CHOICES = [
        (time(9, 0), '09:00'),
        (time(14, 0), '14:00'),
    ]
    HORA_SALIDA_CHOICES = [
        (time(13, 0), '13:00'),
        (time(18, 0), '18:00'),
    ]
    hora_entrada = models.TimeField(choices=HORA_ENTRADA_CHOICES)
    hora_salida = models.TimeField(choices=HORA_SALIDA_CHOICES)
    cantidad_personal = models.IntegerField(default=1)


    def __str__(self):
        return f"Horario {self.turno} {self.hora_entrada} - {self.dia}"

class AsignacionHorario(models.Model):
    id_empl = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    id_horario = models.ForeignKey(Horarios, on_delete=models.CASCADE)
    fecha_asignacion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Asignación de {self.empleado.nombre} {self.empleado.apellido} - {self.horario.dia} {self.horario.turno}"