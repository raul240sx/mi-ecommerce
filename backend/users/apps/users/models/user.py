from django.apps import apps
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

from simple_history.models import HistoricalRecords




class UserManager(BaseUserManager):
    """Manager personalizado para el modelo User."""

    def get_queryset(self):
        """Devuelve solo usuarios activos por defecto."""
        return super().get_queryset().filter(is_active=True)
    
    def create_user(self, email, password=None, **extra_fields):
        """Crea y guarda un usuario normal."""
        if not email:
            raise ValueError('El email debe ser obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """Crea y guarda un superusuario."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField('Nombre', max_length=100, blank=True)
    last_name = models.CharField('Apellido', max_length=100, blank=True)
    phone = models.CharField('Número celular',max_length=9, blank=True)

    # Informacion de si el usuario está activo y si es superusuario
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Registro de quien y cuando se borró
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.SET_NULL, related_name='deleted_users'
    )

    # Fecha de registro en la plataforma
    date_joined = models.DateTimeField(default=timezone.now)

    # Manager
    objects = UserManager()

    # Histórico de cambios
    history = HistoricalRecords()

    # Configuracion de Login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.email
    
    @property
    def is_profile_complete(self):
        """Verifica si el perfil del usuario está completo y si ha añadido por lo menos una dirección"""

        Address = apps.get_model('users', 'Address')
        
        has_name = self.first_name and self.last_name #truthy y falsy
        has_phone = bool(self.phone)
        has_address = Address.objects.filter(user=self).exists()
        return has_name and has_phone and has_address
    
    def soft_delete(self, actor=None):
        """Realiza un borrado lógico del usuario."""

        self.is_active = False
        self.deleted_at = timezone.now()
        if actor:
            self.deleted_by = actor
        self.save()

    def delete(self, using= None, keep_parents=False):
        """Sobrescribe delete() para realizar borrado lógico."""
        self.soft_delete()
