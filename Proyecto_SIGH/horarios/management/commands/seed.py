import random
from datetime import time, date, timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from horarios.models import (
    Profesor, Estudiante, Materia, Aula,
    Grupo, DisponibilidadProfesor, Sesion, Asistencia,
)

# semilla fija para que los datos sean iguales cada vez que corremos el seed
random.seed(42)

# Dias de lunes a viernes
DIAS = ['LUN', 'MAR', 'MIE', 'JUE', 'VIE']

# Bloques de horario tipicos de la facultad
BLOQUES = [
    (time(7, 0), time(9, 0)),
    (time(9, 0), time(11, 0)),
    (time(11, 0), time(13, 0)),
    (time(13, 0), time(15, 0)),
]

# Materias reales que se cursan en Informatica UAQ
MATERIAS = [
    ('Calculo Diferencial',         'MAT-101', 8),
    ('Programacion I',              'INF-101', 8),
    ('Algebra Lineal',              'MAT-102', 6),
    ('Fundamentos de Redes',        'INF-201', 6),
    ('Bases de Datos',              'INF-202', 8),
    ('Programacion Orientada a Objetos', 'INF-203', 8),
    ('Sistemas Operativos',         'INF-301', 6),
    ('Ingenieria de Software',      'INF-302', 6),
    ('Desarrollo Web',              'INF-401', 8),
]

# Profes con nombres tipicos de la facultad
PROFES_NOMBRES = [
    ('Carlos',  'Ramirez Torres'),
    ('Maria',   'Lopez Hernandez'),
    ('Juan',    'Garcia Mendoza'),
    ('Ana',     'Martinez Ruiz'),
    ('Roberto', 'Sanchez Perez'),
    ('Laura',   'Jimenez Castro'),
]

# Aulas del edificio de la facultad
AULAS = [
    ('LAB-A',  'Laboratorio de Computo A', 'FISICA', 30, 'Proyector, 30 PCs, pizarron'),
    ('LAB-B',  'Laboratorio de Computo B', 'FISICA', 30, 'Proyector, 30 PCs, pizarron'),
    ('SALON-1','Salon 101',               'FISICA', 40, 'Proyector, pizarron'),
    ('SALON-2','Salon 102',               'FISICA', 40, 'Proyector, pizarron'),
    ('SALON-3','Salon 201',               'FISICA', 35, 'Canion, pizarron'),
]


class Command(BaseCommand):
    help = 'Llena la base de datos con datos de prueba para el SIGH'

    def handle(self, *args, **options):
        print('Borrando datos anteriores...')
        Asistencia.objects.all().delete()
        Sesion.objects.all().delete()
        DisponibilidadProfesor.objects.all().delete()
        Grupo.objects.all().delete()
        Aula.objects.all().delete()
        Materia.objects.all().delete()
        Estudiante.objects.all().delete()
        Profesor.objects.all().delete()
        User.objects.filter(username__startswith='prof_').delete()
        User.objects.filter(username__startswith='est_').delete()
        print('Datos borrados')

        with transaction.atomic():

            # 1. Crear profes
            print('Creando profesores...')
            profesores = []
            for i, (nombre, apellido) in enumerate(PROFES_NOMBRES):
                usuario = User.objects.create_user(
                    username=f'prof_{i+1:02d}',
                    password='sigh2026',
                    first_name=nombre,
                    last_name=apellido,
                    email=f'prof_{i+1:02d}@uaq.mx',
                )
                prof = Profesor.objects.create(
                    usuario=usuario,
                    numero_empleado=f'UAQ-{i+1:03d}',
                    facultad='Facultad de Informatica',
                    especialidad='Ingenieria en Software',
                )
                profesores.append(prof)
            print(f'{len(profesores)} profesores creados')

            # 2. Crear disponibilidad de cada profe (lunes a viernes, todos los bloques)
            print('Creando disponibilidades...')
            for prof in profesores:
                for dia in DIAS:
                    for hora_ini, hora_fin in BLOQUES:
                        DisponibilidadProfesor.objects.create(
                            profesor=prof,
                            dia=dia,
                            hora_inicio=hora_ini,
                            hora_fin=hora_fin,
                        )
            print('Disponibilidades creadas')

            # 3. Crear estudiantes (18 alumnos)
            print('Creando estudiantes...')
            nombres_alumnos = [
                ('Diego',    'Morales'),  ('Sofia',    'Torres'),
                ('Emilio',   'Vargas'),   ('Valeria',  'Rios'),
                ('Andres',   'Luna'),     ('Camila',   'Reyes'),
                ('Fernando', 'Ibarra'),   ('Mariana',  'Delgado'),
                ('Miguel',   'Soto'),     ('Isabella', 'Medina'),
                ('Rodrigo',  'Flores'),   ('Daniela',  'Guerrero'),
                ('Sebastian','Castro'),   ('Fernanda', 'Ortiz'),
                ('Mateo',    'Romero'),   ('Lucia',    'Navarro'),
                ('Alejandro','Herrera'),  ('Renata',   'Pacheco'),
            ]
            estudiantes = []
            for i, (nombre, apellido) in enumerate(nombres_alumnos):
                usuario = User.objects.create_user(
                    username=f'est_{i+1:02d}',
                    password='sigh2026',
                    first_name=nombre,
                    last_name=apellido,
                    email=f'est_{i+1:02d}@uaq.mx',
                )
                est = Estudiante.objects.create(
                    usuario=usuario,
                    matricula=f'218{i+1:04d}',
                    facultad='Facultad de Informatica',
                    semestre=random.choice([3, 4, 5]),
                )
                estudiantes.append(est)
            print(f'{len(estudiantes)} estudiantes creados')

            # 4. Crear aulas
            print('Creando aulas...')
            aulas = []
            for codigo, nombre, tipo, capacidad, equipo in AULAS:
                aula = Aula.objects.create(
                    codigo=codigo,
                    nombre=nombre,
                    tipo=tipo,
                    capacidad=capacidad,
                    equipo=equipo,
                )
                aulas.append(aula)
            print(f'{len(aulas)} aulas creadas')

            # 5. Crear materias
            print('Creando materias...')
            materias = []
            for nombre, codigo, creditos in MATERIAS:
                mat = Materia.objects.create(
                    nombre=nombre,
                    codigo=codigo,
                    facultad='Facultad de Informatica',
                    creditos=creditos,
                )
                materias.append(mat)
            print(f'{len(materias)} materias creadas')

            # 6. Crear 3 grupos, uno por cada par materia-profe
            # cada grupo tiene 6 alumnos
            print('Creando grupos...')
            grupos = []
            for i in range(3):
                grupo = Grupo.objects.create(
                    nombre=f'G-{i+1:02d}',
                    materia=materias[i],
                    profesor=profesores[i],
                    periodo='2026-1',
                    cupo_maximo=30,
                )
                # asignamos 6 alumnos a cada grupo
                alumnos_del_grupo = estudiantes[i*6 : i*6 + 6]
                grupo.estudiantes.set(alumnos_del_grupo)
                grupos.append(grupo)
            print(f'{len(grupos)} grupos creados')

            # 7. Crear sesiones: cada grupo tiene clase 3 dias a la semana en distintos bloques
            # aula fija por grupo para no tener choques
            print('Creando sesiones...')
            sesiones_creadas = 0
            dias_por_grupo = [
                ['LUN', 'MIE', 'VIE'],
                ['MAR', 'JUE', 'VIE'],
                ['LUN', 'MAR', 'JUE'],
            ]
            for i, grupo in enumerate(grupos):
                aula_asignada = aulas[i]
                for dia in dias_por_grupo[i]:
                    Sesion.objects.create(
                        grupo=grupo,
                        aula=aula_asignada,
                        tipo='CLASE',
                        dia=dia,
                        hora_inicio=BLOQUES[0][0],
                        hora_fin=BLOQUES[0][1],
                        fecha_inicio=date(2026, 1, 12),
                        fecha_fin=date(2026, 5, 30),
                    )
                    sesiones_creadas += 1

                # tambien creamos un examen parcial (tipo EXAMEN)
                Sesion.objects.create(
                    grupo=grupo,
                    aula=aula_asignada,
                    tipo='EXAMEN',
                    dia='SAB',
                    hora_inicio=time(9, 0),
                    hora_fin=time(11, 0),
                    fecha_inicio=date(2026, 3, 14),
                    fecha_fin=date(2026, 3, 14),
                )
                sesiones_creadas += 1
            print(f'{sesiones_creadas} sesiones creadas')

            # 8. Crear asistencias para cada sesion
            # 80% de los alumnos van a cada clase
            print('Creando asistencias...')
            total_asistencias = 0
            todas_las_sesiones = list(Sesion.objects.filter(tipo='CLASE'))
            for sesion in todas_las_sesiones:
                alumnos_inscritos = list(sesion.grupo.estudiantes.all())
                for alumno in alumnos_inscritos:
                    # el 80% va, el 20% falta
                    if random.random() < 0.80:
                        estado = 'PRESENTE'
                        nota = None
                    else:
                        estado = 'AUSENTE'
                        nota = 'No se presento sin aviso'
                    Asistencia.objects.create(
                        sesion=sesion,
                        estudiante=alumno,
                        fecha=date(2026, 2, 3),
                        estado=estado,
                        observacion=nota,
                    )
                    total_asistencias += 1
            print(f'{total_asistencias} asistencias registradas')

        # resumen de lo que quedo en la BD
        print('')
        print('===== SEED COMPLETADO =====')
        print(f'Profesores:      {Profesor.objects.count()}')
        print(f'Estudiantes:     {Estudiante.objects.count()}')
        print(f'Materias:        {Materia.objects.count()}')
        print(f'Aulas:           {Aula.objects.count()}')
        print(f'Grupos:          {Grupo.objects.count()}')
        print(f'Sesiones:        {Sesion.objects.count()}')
        print(f'Asistencias:     {Asistencia.objects.count()}')
        print('')
        print('Contrasena de todos: sigh2026')
        print('Profesores: prof_01 a prof_06')
        print('Estudiantes: est_01 a est_18')
