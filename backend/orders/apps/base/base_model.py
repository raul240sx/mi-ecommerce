from django.db import models
from django.utils import timezone


ADMIN_USER_ID = -1

class BaseModel(models.Model):
    state = models.BooleanField('Estado', default=True)
    created_date = models.DateTimeField('Fecha de creación', auto_now_add=True)
    created_by = models.IntegerField('Creado por', blank=True, null=True)
    modified_date = models.DateTimeField('Fecha de modificación', auto_now=True)
    modified_by = models.IntegerField('Modificado por', blank=True, null=True)
    deleted_date = models.DateTimeField('Fecha de eliminación', null=True, blank=True)
    deleted_by = models.IntegerField('Eliminado por', blank=True, null=True)


    def save(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)

        if user_id is None:
            user_id = ADMIN_USER_ID

        if user_id is not None:
            if self.state:
                if self.pk:
                    self.modified_by = user_id
                else:
                    self.created_by = user_id

            else:
                self.deleted_by = user_id       

        super().save(*args, **kwargs)
    

        

    def delete(self, *args, **kwargs):
        self.state = False
        self.deleted_date = timezone.now()
        self.save(user_id=kwargs.get('user_id'))



    class Meta:
        abstract = True
        verbose_name = 'Modelo base'
        verbose_name_plural = 'Modelos base'
        abstract = True
        indexes = [
            models.Index(fields=['created_date'])
        ]
