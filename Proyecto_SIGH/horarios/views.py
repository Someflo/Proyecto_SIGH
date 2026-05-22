from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Sesion, Grupo, Estudiante, Asistencia, Notificacion, Profesor


def es_profesor(usuario):
    return hasattr(usuario, 'perfil_profesor')


def es_alumno(usuario):
    return hasattr(usuario, 'perfil_estudiante')


def asignar_horarios_por_dia(grupos):
    """Asigna atributos .lun, .mar, .mie, .jue, .vie a cada grupo
    con las horas de sus sesiones, para que el template pueda usarlos."""
    dias_map = {
        'LUN': 'lun', 'MAR': 'mar', 'MIE': 'mie',
        'JUE': 'jue', 'VIE': 'vie', 'SAB': 'sab',
    }
    for grupo in grupos:
        for attr in dias_map.values():
            setattr(grupo, attr, '')
        for sesion in grupo.sesiones.all():
            attr = dias_map.get(sesion.dia, '')
            if attr:
                hora = f"{sesion.hora_inicio.strftime('%H:%M')}-{sesion.hora_fin.strftime('%H:%M')}"
                setattr(grupo, attr, hora)
    return grupos


@login_required
def ver_horario(request):

    if es_profesor(request.user):

        profesor = request.user.perfil_profesor

        total_materias = profesor.grupos.values('materia').distinct().count()

        grupos = list(profesor.grupos.all())

        asignar_horarios_por_dia(grupos)

        sesiones = Sesion.objects.filter(
            grupo__in=grupos
        )

        notificaciones = Notificacion.objects.filter(
            usuario=request.user
        )

        contexto = {
            'profesor': profesor,
            'grupos': grupos,
            'sesiones': sesiones,
            'notificaciones': notificaciones,
            'total_materias': total_materias,
        }

        return render(
            request,
            'DashboardMaestros.html',
            contexto
        )

    elif es_alumno(request.user):

        estudiante = get_object_or_404(
            Estudiante,
            usuario=request.user
        )

        grupos_qs = estudiante.grupos.all()

        total_materias = grupos_qs.values('materia').distinct().count()

        grupos = list(grupos_qs)

        asignar_horarios_por_dia(grupos)

        sesiones = Sesion.objects.filter(
            grupo__in=grupos
        )

        notificaciones = Notificacion.objects.filter(
            usuario=request.user
        )

        # Asistencias agrupadas por grupo/materia para mostrar en el dashboard
        resumen_asistencias = []
        for grupo in grupos:
            total_sesiones = grupo.sesiones.count()
            presentes = Asistencia.objects.filter(
                estudiante=estudiante,
                sesion__grupo=grupo,
                estado='PRESENTE'
            ).count()
            porcentaje = round((presentes / total_sesiones * 100), 1) if total_sesiones > 0 else 0
            resumen_asistencias.append({
                'materia': grupo.materia.nombre,
                'docente': grupo.profesor.usuario.get_full_name(),
                'total_asistencias': f"{presentes} / {total_sesiones}",
                'porcentaje': porcentaje,
            })

        contexto = {
            'estudiante': estudiante,
            'grupos': grupos,
            'sesiones': sesiones,
            'notificaciones': notificaciones,
            'total_materias': total_materias,
            'asistencias': resumen_asistencias,
        }

        return render(
            request,
            'DashboardAlumnos.html',
            contexto
        )

    else:

        messages.error(
            request,
            'No tienes permiso para ver esta página.'
        )

        return redirect('login')




@login_required
def ver_asistencias(request, sesion_id):

    sesion = get_object_or_404(
        Sesion,
        id=sesion_id
    )

    if es_profesor(request.user):

        profesor = request.user.perfil_profesor

        if not profesor.grupos.filter(id=sesion.grupo.id).exists():

            messages.error(
                request,
                'No tienes permiso para ver esta sesión.'
            )

            return redirect('dashboard')

        asistencias = Asistencia.objects.filter(
            sesion=sesion
        )

    elif es_alumno(request.user):

        estudiante = get_object_or_404(
            Estudiante,
            usuario=request.user
        )

        if not estudiante.grupos.filter(
            id=sesion.grupo.id
        ).exists():

            messages.error(
                request,
                'No tienes permiso para ver esta sesión.'
            )

            return redirect('dashboard')

        asistencias = Asistencia.objects.filter(
            sesion=sesion,
            estudiante=estudiante
        )

    else:

        messages.error(
            request,
            'No tienes permiso para ver esta página.'
        )

        return redirect('login')

    contexto = {
        'sesion': sesion,
        'asistencias': asistencias,
    }

    return render(
        request,
        'ver_asistencias.html',
        contexto
    )


@login_required
def registrar_asistencia(request, sesion_id):

    sesion = get_object_or_404(
        Sesion,
        id=sesion_id
    )

    if es_profesor(request.user):

        profesor = request.user.perfil_profesor

        if not profesor.grupos.filter(
            id=sesion.grupo.id
        ).exists():

            messages.error(
                request,
                'No tienes permiso para esta sesión.'
            )

            return redirect('dashboard')

        estudiantes = sesion.grupo.estudiantes.all()

        if request.method == 'POST':

            for alumno in estudiantes:

                estado = request.POST.get(
                    f'estado_{alumno.id}',
                    'AUSENTE'
                )

                observacion = request.POST.get(
                    f'observacion_{alumno.id}',
                    ''
                )

                asistencia, creada = Asistencia.objects.get_or_create(
                    sesion=sesion,
                    estudiante=alumno,
                    fecha=timezone.now().date()
                )

                asistencia.estado = estado
                asistencia.observacion = observacion

                asistencia.save()

            messages.success(
                request,
                '¡Asistencia registrada correctamente!'
            )

            return redirect(
                'ver_asistencias',
                sesion_id=sesion.id
            )

        contexto = {
            'sesion': sesion,
            'estudiantes': estudiantes,
        }

        return render(
            request,
            'registrar_asistencia.html',
            contexto
        )

    elif es_alumno(request.user):

        messages.error(
            request,
            'Solo los profesores pueden registrar asistencias.'
        )

        return redirect('dashboard')

    else:

        messages.error(
            request,
            'No tienes permiso para ver esta página.'
        )

        return redirect('login')


def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:

            login(
                request,
                usuario
            )

            messages.success(
                request,
                f'¡Bienvenido, {usuario.username}!'
            )

            return redirect('dashboard')

        else:

            messages.error(
                request,
                'Usuario o contraseña incorrectos.'
            )

    return render(
        request,
        'loginMaestros.html'
    )


@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        'Has cerrado sesión correctamente.'
    )

    return redirect('login')



