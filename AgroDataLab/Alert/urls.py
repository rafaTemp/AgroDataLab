from django.urls import path
from . import views

urlpatterns = [
    path("", views.AlertListView.as_view(), name="alert_list"),
    path("crear/", views.AlertCreateView.as_view(), name="alert_create"),
    path("editar/<int:pk>/", views.AlertUpdateView.as_view(), name="alert_update"),
    path("eliminar/<int:pk>/", views.AlertDeleteView.as_view(), name="alert_delete"),
]
