from django.db import models

from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel



class Category(BaseModel):
    name = models.CharField('Categoría', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):
        return self.name