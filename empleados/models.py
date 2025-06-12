from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
def validar_mayor_18(value):
    hoy = timezone.now().date()
    edad = hoy.year - value.year - ((hoy.month, hoy.day) < (value.month, value.day))
    if edad < 18:
        raise ValidationError('El empleado debe ser mayor de 18 años.')

class Empleado(models.Model):
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
    id_empl = models.ForeignKey('Empleado', on_delete=models.CASCADE, related_name='horarios')
    turno = models.CharField(max_length=20, choices=[('Mañana', 'Mañana'), ('Tarde', 'Tarde')], default='Mañana')
    dia = models.CharField(max_length=10, choices=[('Lunes', 'Lunes'), ('Martes', 'Martes'), ('Miércoles', 'Miércoles'), ('Jueves', 'Jueves'), ('Viernes', 'Viernes')])
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()
    cantidad_personal = models.IntegerField(default=1)


    def __str__(self):
        return f"Horario {self.id_empl.nombre} {self.id_empl.apellido} - {self.dia}"
