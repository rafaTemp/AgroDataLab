from django.db import models


class EnviroProRecord(models.Model):
    fecha_hora = models.DateTimeField()

    humedad_media = models.FloatField(null=True, blank=True)
    humedad_minima = models.FloatField(null=True, blank=True)
    humedad_maxima = models.FloatField(null=True, blank=True)

    temperatura_media = models.FloatField(null=True, blank=True)
    temperatura_minima = models.FloatField(null=True, blank=True)
    temperatura_maxima = models.FloatField(null=True, blank=True)

    bateria_mv = models.FloatField(null=True, blank=True)
    panel_solar_mv = models.FloatField(null=True, blank=True)

    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha_hora']

    def __str__(self):
        return f"Registro EnviroPro - {self.fecha_hora}"