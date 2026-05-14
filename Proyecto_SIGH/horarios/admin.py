from django.contrib import admin
from .models import (
    Profesor, Estudiante, Materia, Aula,
    Grupo, DisponibilidadProfesor, Sesion, Asistencia
)

# Así configuran qué columnas ve el administrador en la tabla
@admin.register(Sesion)
class SesionAdmin(admin.ModelAdmin):
    # Columnas que aparecen en la tabla
    list_display = ('grupo', 'aula', 'dia', 'hora_inicio', 'hora_fin') 
    
    # Filtros laterales automáticos
    list_filter = ('dia', 'aula', 'grupo') 
    
    # Barra de búsqueda arriba
    search_fields = ('grupo__materia__nombre', 'aula__nombre') 

# Registran los demás de forma sencilla
admin.site.register(Profesor)
admin.site.register(Estudiante)
admin.site.register(Materia)
admin.site.register(DisponibilidadProfesor)
admin.site.register(Aula)
admin.site.register(Grupo)
admin.site.register(Asistencia)