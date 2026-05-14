from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio_enviro'),
    path("importar/", views.importar_csv, name="importar_csv"),
    path("resultado/", views.resultado_enviro, name="resultado_enviro"),
]