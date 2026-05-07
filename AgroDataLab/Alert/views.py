from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Alert

# LISTAR: Muestra todas las alertas
class AlertListView(ListView):
    model = Alert
    template_name = 'list.html'
    context_object_name = 'alertas'
    ordering = ['-fecha']  # De más reciente a más antigua

# CREAR: Formulario para nueva alerta
class AlertCreateView(CreateView):
    model = Alert
    template_name = 'form.html'
    fields = ['tipo_de_alerta', 'descripcion', 'variable_afectada']
    success_url = reverse_lazy('alert_list')

# EDITAR: Modificar alerta existente
class AlertUpdateView(UpdateView):
    model = Alert
    template_name = 'form.html'
    fields = ['tipo_de_alerta', 'descripcion', 'variable_afectada']
    success_url = reverse_lazy('alert_list')

# ELIMINAR: Borrar alerta
class AlertDeleteView(DeleteView):  
    model = Alert
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('alert_list')