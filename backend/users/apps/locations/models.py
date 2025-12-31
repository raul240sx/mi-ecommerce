from django.db import models

###########################################################################
                ### MODELO REGION ###
###########################################################################
class Region(models.Model):
    ZONE_NORTH = 'NORTH'
    ZONE_CENTER = 'CENTER'
    ZONE_SOUTH = 'SOUTH'

    ZONE_CHOICES = [
        (ZONE_NORTH, 'Zona Norte'),
        (ZONE_CENTER, 'Zona Centro'),
        (ZONE_SOUTH, 'Zona Sur'),
    ]

    name = models.CharField(max_length=100, unique=True)
    zone = models.CharField(max_length=10, choices=ZONE_CHOICES, db_index=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Región'
        verbose_name_plural = 'Regiones'


    def __str__(self):
        return f'{self.name} ({self.get_zone_display()})'


###########################################################################
                ### MODELO COMUNA ###
###########################################################################
class Commune(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="comunas") 


    class Meta:
        ordering = ['name']
        verbose_name = 'Comuna'
        verbose_name_plural = 'Comunas'
        constraints = [
            models.UniqueConstraint(fields=['name', 'region'],
            name='unique_comuna_region')
        ]
        indexes = [
            models.Index(fields=['region', 'name']),
        ]

    def __str__(self):
        return f'{self.name} - {self.region.name}'
