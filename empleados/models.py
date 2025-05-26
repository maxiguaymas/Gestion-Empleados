from django.db import models

# Create your models here.

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.IntegerField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], default='O')
    estado_civil = models.CharField(max_length=20, choices=[('Soltero', 'Soltero'), ('Casado', 'Casado'), ('Divorciado', 'Divorciado'), ('Viudo', 'Viudo')], default='Soltero')
    fecha_nacimiento = models.DateField()
    estado = models.CharField(max_length=20, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo'), ('Suspendido', 'Suspendido'), ('Licencia', 'Licencia')], default='Activo')
    fecha_ingreso = models.DateField(auto_now_add=True)
    fecha_egreso = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.dni}"
    
    
