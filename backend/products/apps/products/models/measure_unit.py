from django.db import models

from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel


class MeasureUnit(BaseModel):
    name = models.CharField('Unidad de medida', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de medida' 


    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):
        return self.name
