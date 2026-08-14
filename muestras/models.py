from django.db import models
from django.contrib.auth.models import User

class Muestra(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, blank=True)
    tipo   = models.CharField(max_length=50)
    foto   = models.ImageField(upload_to='muestras_fotos/', blank=True, null=True)
    
    responsable = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.codigo:
            prefijo = ''
            tipo_norm = self.tipo.strip().lower()

            # Usamos 'in' para buscar la palabra clave dentro de lo que envía React Native
            # Ej: Si envían "Bebida azucarada", entra en AL
            if 'alimento' in tipo_norm or 'bebida' in tipo_norm or 'superficie' in tipo_norm:
                prefijo = 'AL'
            elif 'agua' in tipo_norm:
                prefijo = 'A'
            elif 'ambiente' in tipo_norm or 'aire' in tipo_norm or 'suelo' in tipo_norm:
                prefijo = 'AM'
            else:
                prefijo = 'GEN'

            # Buscamos la última muestra que tenga este mismo prefijo
            ultima_muestra = Muestra.objects.filter(codigo__startswith=f"{prefijo}-").order_by('id').last()

            if ultima_muestra:
                try:
                    ultimo_numero = int(ultima_muestra.codigo.split('-')[1])
                    nuevo_numero = ultimo_numero + 1
                except (IndexError, ValueError):
                    nuevo_numero = 1
            else:
                nuevo_numero = 1

            # Asignamos el formato XXXX
            self.codigo = f"{prefijo}-{nuevo_numero:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} — {self.nombre}"