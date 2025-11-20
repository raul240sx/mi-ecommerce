from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    state = models.BooleanField('Estado', default=True)
    created_date = models.DateTimeField('Fecha de creación', auto_now_add=True)
    modified_date = models.DateTimeField('Fecha de modificación', auto_now=True)
    deleted_date = models.DateTimeField('Fecha de eliminación', null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = 'Modelo base'
        verbose_name_plural = 'Modelos base'
                                                        