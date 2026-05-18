from django.contrib import admin
from django.urls import path, include
from Core import views as core_views

urlpatterns = [
    path('', core_views.dashboard, name='dashboard'),
    path('registro/', core_views.register, name='register'),
    path('acerca/', core_views.about, name='about'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('enviro/', include('EnviroProRecord.urls')),
    path('alerta/', include('Alert.urls')),
    path('recomendacion/', include('Recommendation.urls')),
]