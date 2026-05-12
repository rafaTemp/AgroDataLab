from django.db import models
from Alert.models import Alert

class Recommendation(models.Model):
    PRIORIDAD_CHOICES = [
        ('Alta', 'Alta'),
        ('Media', 'Media'),
        ('Baja', 'Baja'),
    ]
    
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Revisada', 'Revisada'),
        ('Descartada', 'Descartada'),
    ]

    titulo = models.CharField(max_length=200, verbose_name="Título")
    descripcion = models.TextField(verbose_name="Descripción")
    alerta = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name="recomendaciones", verbose_name="Alerta relacionada")
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, verbose_name="Prioridad")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente', verbose_name="Estado")

    def __str__(self):
        return f"{self.titulo} - {self.estado}"
    
    class Meta:
        db_table = "recomendacion"
