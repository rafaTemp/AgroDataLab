from django.db import models
tipo_de_alerta_choices = [
    ("Humedad_alta", "Humedad alta en el suelo"),
    ("Humedad_baja", "Humedad baja en el suelo"),
]
class Alert(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    tipo_de_alerta = models.CharField(max_length=100, verbose_name="Tipo de alerta", choices=tipo_de_alerta_choices)
    nivel = models.CharField(max_length=50, verbose_name="Nivel")
    descripcion = models.TextField(verbose_name="Descripción")
    variable_afectada = models.CharField(max_length=100, verbose_name="Variable afectada")

    def __str__(self):
        return f"{self.tipo_de_alerta} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"
    
    class Meta:
        db_table = "alerta"