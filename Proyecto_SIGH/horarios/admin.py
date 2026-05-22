from django.contrib import admin
from .models import (
    Profesor, Estudiante, Materia, Aula,
    Grupo, DisponibilidadProfesor, Sesion, Asistencia, Notificacion
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
@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'sesion', 'fecha', 'estado')
    list_filter = ('estado', 'fecha', 'estudiante')
    search_fields = ('estudiante__usuario__username', 'estudiante__matricula', 'sesion__grupo__nombre')

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'mensaje', 'fecha', 'leida')
    list_filter = ('tipo', 'leida')
    search_fields = ('usuario__username', 'mensaje')
    list_editable = ('leida',)
    actions = ['marcar_como_leidas']

    def marcar_como_leidas(self, request, queryset):
        queryset.update(leida=True)
    marcar_como_leidas.short_description = "Marcar seleccionadas como leídas"