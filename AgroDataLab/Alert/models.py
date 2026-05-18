from django.db import models
tipo_de_alerta_choices = [
    ("Humedad_alta", "Humedad alta en el suelo"),
    ("Humedad_baja", "Humedad baja en el suelo"),
    ("Bateria_critica", "Batería crítica"),
    ("Caida_bateria", "Caída brusca de batería"),
    ("Panel_sin_carga", "Panel solar sin carga y batería baja"),
]

variable_afectada_choices = [
    ("humedad_media", "Humedad Media"),
    ("humedad_minima", "Humedad Mínima"),
    ("humedad_maxima", "Humedad Máxima"),
    ("temperatura_media", "Temperatura Media"),
    ("temperatura_minima", "Temperatura Mínima"),
    ("temperatura_maxima", "Temperatura Máxima"),
    ("bateria_mv", "Batería (mV)"),
    ("panel_solar_mv", "Panel Solar (mV)"),
]

class Alert(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    tipo_de_alerta = models.CharField(max_length=100, verbose_name="Tipo de alerta", choices=tipo_de_alerta_choices)
    descripcion = models.TextField(verbose_name="Descripción")
    variable_afectada = models.CharField(
        max_length=100, 
        verbose_name="Variable afectada",
        choices=variable_afectada_choices
    )

    def __str__(self):
        return f"{self.tipo_de_alerta} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"
    
    class Meta:
        db_table = "alerta"