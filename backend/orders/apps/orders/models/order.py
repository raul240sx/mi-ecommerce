from django.db import models

from simple_history.models import HistoricalRecords

from apps.base.base_model import BaseModel


class Order(BaseModel):

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        PAID = 'PAID', 'Pagado'
        CANCELLED = 'CANCELLED', 'Cancelado'


    user_id = models.IntegerField('Orden del usuario')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    total_amount = models.DecimalField('Total orden', max_digits=8, decimal_places=0)


    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Ordenes'


    history = HistoricalRecords(user_db_constraint=False)


    def __str__(self):
        return f'Orden Nro. {self.pk} - Usuario {self.user_id}'