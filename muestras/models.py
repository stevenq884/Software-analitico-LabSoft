from django.db import models

class Muestra(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20)
    tipo   = models.CharField(max_length=50)
    foto   = models.ImageField(upload_to='muestras_fotos/', blank=True, null=True)

    def __str__(self):
        return f"{self.codigo} — {self.nombre}"