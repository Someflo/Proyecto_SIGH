from django.shortcuts import render
from .models import (
    Profesor, Estudiante, Materia, Aula,
    Grupo, Sesion, Asistencia,
)

# pagina principal con los conteos de la base de datos
def dashboard_view(request):
    contexto = {
        'total_profesores': Profesor.objects.count(),
        'total_estudiantes': Estudiante.objects.count(),
        'total_materias': Materia.objects.count(),
        'total_aulas': Aula.objects.count(),
        'total_grupos': Grupo.objects.count(),
        'total_sesiones': Sesion.objects.count(),
        'total_asistencias': Asistencia.objects.count(),
    }
    return render(request, 'horarios/dashboard.html', contexto)
