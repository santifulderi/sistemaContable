from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

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
    # id_perfil = models.ForeignKey('TipoPerfiles', models.DO_NOTHING, db_column='id_perfil')
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
