from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Recommendation

# LISTAR: Muestra todas las recomendaciones
class RecommendationListView(ListView):
    model = Recommendation
    template_name = 'recommendation_list.html'
    context_object_name = 'recomendaciones'

# CREAR: Formulario para nueva recomendación
class RecommendationCreateView(CreateView):
    model = Recommendation
    template_name = 'recommendation_form.html'
    fields = ['titulo', 'descripcion', 'alerta', 'prioridad', 'estado']
    success_url = reverse_lazy('recommendation_list')

# EDITAR: Modificar recomendación existente
class RecommendationUpdateView(UpdateView):
    model = Recommendation
    template_name = 'recommendation_form.html'
    fields = ['titulo', 'descripcion', 'alerta', 'prioridad', 'estado']
    success_url = reverse_lazy('recommendation_list')

# ELIMINAR: Borrar recomendación
class RecommendationDeleteView(DeleteView):  
    model = Recommendation
    template_name = 'recommendation_confirm_delete.html'
    success_url = reverse_lazy('recommendation_list')
