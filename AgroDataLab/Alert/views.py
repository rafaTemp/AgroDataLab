from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Alert

# LISTAR: Muestra todas las alertas
class AlertListView(LoginRequiredMixin, ListView):
    model = Alert
    template_name = 'list.html'
    context_object_name = 'alertas'
    ordering = ['-fecha']  # De más reciente a más antigua

# CREAR: Formulario para nueva alerta
class AlertCreateView(LoginRequiredMixin, CreateView):
    model = Alert
    template_name = 'form.html'
    fields = ['tipo_de_alerta', 'descripcion', 'variable_afectada']
    success_url = reverse_lazy('alert_list')

# EDITAR: Modificar alerta existente
class AlertUpdateView(LoginRequiredMixin, UpdateView):
    model = Alert
    template_name = 'form.html'
    fields = ['tipo_de_alerta', 'descripcion', 'variable_afectada']
    success_url = reverse_lazy('alert_list')

# ELIMINAR: Borrar alerta
class AlertDeleteView(LoginRequiredMixin, DeleteView):  
    model = Alert
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('alert_list')
