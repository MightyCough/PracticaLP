from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
# Create your models here.

class Cliente(models.Model):
    ##id clave primaria por default
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
       return f"{self.nombre} {self.apellidos}"
   


class Vehiculo(models.Model):
    marca=models.CharField(max_length=45)
    modelo=models.CharField(max_length=45)
    anio = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10,decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    disponible = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.marca} {self.modelo} {self.anio} - {self.precio}"
    
class Vendedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    vehiculos = models.ManyToManyField(Vehiculo, related_name='vendedores')  # Relación con vehículos

    def __str__(self):
        return self.nombre    

class Cita(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha_cita = models.DateTimeField()
    notas = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=50,choices=[
            ('pendiente', 'Pendiente'),
            ('confirmada', 'Confirmada'),
            ('cancelada', 'Cancelada'),
        ],
        default='pendiente',
    )
    
    def clean(self):
        #validacion para que la fecha de la cita no sea en el pasado
        if self.fecha_cita < timezone.now():
            raise ValueError("La fecha de la cita no puede estar en el pasado")
    
    def __str__(self):
       return f"Cita con {self.cliente} para {self.vehiculo} el {self.fecha_cita.strftime('%Y-%m-%d %H:%M')}"
   
   
class UsuarioManager(BaseUserManager):
    def create_user(self,username,email,password=None,**extra_fields):
        ##Creamos un usuario en base a nombre de usuario, contraseña y correo
        if not email:
            raise ValueError("Error el email es obligatorio")
        email=self.normalize_email(email)
        user = self.model(username=username,email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username,email,password=None,**extra_fields):
        ##creamos un superusuario en base a nombre, contraseña y correo
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("El campo staff debe ser True")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El campo superusuario debe ser True")
        
        return self.create_user(username,email,password,**extra_fields)
    
class Usuario(AbstractUser):
    objects = UsuarioManager()
    
    def __str__(self):
        return self.username