from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils import timezone

# Create your models here.


class UsuarioManager(BaseUserManager):
    def create_user(self, email, username, nombres, apellidos, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')

        usuario = self.model(
            username=username,
            email=self.normalize_email(email),
            nombres=nombres,
            apellidos=apellidos
        )

        usuario.set_password(password) # encripta la contraseña y la guarda en ese campo
        usuario.save()
        return usuario

    def create_superuser(self, email, username, nombres, apellidos, password):
        usuario = self.create_user(
            email,
            username=username,
            nombres=nombres,
            apellidos=apellidos,
            password=password
        )
        usuario.usuario_administrador = True
        usuario.save()
        return usuario


class Usuario(AbstractBaseUser):
    username = models.CharField('Nombre de usuario', unique=True, max_length=100)
    email = models.EmailField('Correo Electrónico', max_length=255, unique=True)
    nombres = models.CharField('Nombres', max_length=200, blank=True, null=True)
    apellidos = models.CharField('Apellidos', max_length=200, blank=True, null=True)
    id_perfil = models.ForeignKey('TipoPerfiles', models.DO_NOTHING, db_column='id_perfil')
    imagen = models.ImageField('Imagen de perfil', upload_to='static/images/perfil/', default='/static/images/perfil/default.png',
                               height_field=None, width_field=None, max_length=200)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    object = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombres', 'apellidos']

    def __str__(self):
        return f"Usuario {self.username}"
        # return f'{self.nombres},{self.apellidos}' PARA RETORNAR DIRECTAMENTE EL NOMBRE Y EL APELLIDO

    def has_perm(self, perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador


class Asiento(models.Model):
    fecha = models.DateField(default=timezone.now)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')

    class Meta:
        # managed = False
        db_table = 'asiento'
        verbose_name_plural = 'Asientos'
        ordering = ['fecha']


class CuentaAsiento(models.Model):
    id_cuenta = models.ForeignKey('Cuentas', models.DO_NOTHING, )
    id_asiento = models.ForeignKey('Asiento', models.DO_NOTHING, )
    debe = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    haber = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    saldo = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'cuenta_asiento'
        verbose_name_plural = 'Cuenta asientos'


class Cuentas(models.Model):
    cuenta = models.CharField(max_length=50)
    codigo = models.CharField(unique=True, max_length=20)
    tipo = models.CharField(max_length=20)
    recibe_saldo = models.BooleanField()
    saldo_actual = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'cuentas'
        verbose_name_plural = 'Cuentas'


class TipoPerfiles(models.Model):
    perfil = models.CharField(max_length=30)

    def __str__(self):
        return f"Tipo de perfil: {self.perfil}"
    class Meta:
        # managed = False
        db_table = 'tipo_perfiles'
        verbose_name_plural = 'Tipos perfiles'


class PerfilesTareas(models.Model):
    id_tipo_perfil = models.ForeignKey('TipoPerfiles', models.DO_NOTHING, db_column='id_perfil')
    id_tarea = models.ForeignKey('Tareas', models.DO_NOTHING, db_column='id_tarea')

    class Meta:
        # managed = False
        db_table = 'perfiles_tareas'
        verbose_name_plural = 'Perfiles tareas'


class Tareas(models.Model):
    tarea = models.CharField(max_length=50)

    class Meta:
        # managed = False
        db_table = 'tareas'
        verbose_name_plural = 'Tareas'
