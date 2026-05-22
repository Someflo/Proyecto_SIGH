from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='Portalinicio.html'), name='portal'),
    path('dashboard/', views.ver_horario, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('sesion/<int:sesion_id>/asistencias/', views.ver_asistencias, name='ver_asistencias'),
    path('sesion/<int:sesion_id>/registrar/', views.registrar_asistencia, name='registrar_asistencia'),
]
