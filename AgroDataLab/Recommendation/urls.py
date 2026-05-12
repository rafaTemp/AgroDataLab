from django.urls import path
from . import views

urlpatterns = [
    path("", views.RecommendationListView.as_view(), name="recommendation_list"),
    path("crear/", views.RecommendationCreateView.as_view(), name="recommendation_create"),
    path("editar/<int:pk>/", views.RecommendationUpdateView.as_view(), name="recommendation_update"),
    path("eliminar/<int:pk>/", views.RecommendationDeleteView.as_view(), name="recommendation_delete"),
]
