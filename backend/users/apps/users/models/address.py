from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone

from simple_history.models import HistoricalRecords


class Address(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='addresses')
    commune = models.ForeignKey('locations.Commune', on_delete=models.PROTECT)
    street = models.CharField('Calle', max_length=100)
    number = models.CharField('Número', max_length=10)
    apartment = models.CharField('Departamento', max_length=10, blank=True, null=True)
    is_main = models.BooleanField('Dirección principal', default=False)


    # Informacion sobre si la direccion está activa e informacion acerca del borrado lógico
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, blank=True, null=True, related_name='deleted_addresses')

    # Historial
    history = HistoricalRecords()


    def reassign_main_address(self):
        new_main_address = Address.objects.select_for_update().filter(user=self.user, is_active=True).exclude(id=self.id).first()

        if new_main_address:
            new_main_address.is_main=True
            new_main_address.save(update_fields=['is_main'])



    def soft_delete(self, actor=None):

        was_main = self.is_main


        self.is_active = False
        self.is_main = False

        self.deleted_at = timezone.now()
        if actor:
            self.deleted_by = actor
        self.save(update_fields=['is_active', 'is_main', 'deleted_at', 'deleted_by'])

        if was_main:
            self.reassign_main_address()



    def delete(self, using=None, keep_parents=False):
        with transaction.atomic():
            self.soft_delete()


    class Meta:
        verbose_name = 'Dirección'
        verbose_name_plural = 'Direcciones'
        ordering = ['user', 'id']
        indexes = [
            models.Index(fields=['user', 'is_main']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=Q(is_main=True, is_active=True),
                name='unique_active_main_address_constraint'
            )
        ]


    def __str__(self):
        return f'{self.street} {self.number}, {self.commune.name}'
