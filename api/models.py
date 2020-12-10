from django.db import models

class Ecuacion(models.Model):
    imagen = models.ImageField(upload_to='ecuaciones', blank=True)
    ecuacion = models.TextField(max_length=360, blank=True)
    solucion = models.TextField(max_length=360, blank=True)