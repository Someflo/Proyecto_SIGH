from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User



# TABLA 1: profesor 

class Profesor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_profesor')
    numero_empleado = models.CharField(max_length=20, unique=True)
    # facultad ya no es una tabla aparte, solo guardamos el nombre
    facultad = models.CharField(max_length=150)
    especialidad = models.CharField(max_length=200, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Profesores'

    def __str__(self):
        return f"{self.usuario.get_full_name()} ({self.numero_empleado})"



#TABLA 2: Estudiante

class Estudiante(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_estudiante')
    matricula = models.CharField(max_length=20, unique=True)
    facultad = models.CharField(max_length=150)
    semestre = models.PositiveSmallIntegerField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Estudiantes'

    def __str__(self):
        return f"{self.matricula} - {self.usuario.get_full_name()}"



#TABLA 3: Materia

class Materia(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=20, unique=True)

    facultad = models.CharField(max_length=150)
    creditos = models.PositiveSmallIntegerField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Materias'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"



#TABLA 4: Aula

class Aula(models.Model):
    TIPO_CHOICES = [
        ('FISICA', 'Física'),
        ('VIRTUAL', 'Virtual'),
    ]

    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    capacidad = models.PositiveIntegerField()
    # campo de texto para anotar el equipo que tiene el aula (proyector, PCs, etc.)
    equipo = models.TextField(null=True, blank=True)
    link_zoom = models.URLField(max_length=500, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Aulas'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    def clean(self):

        if self.tipo == 'VIRTUAL' and not self.link_zoom:
            raise ValidationError('Las aulas virtuales necesitan un link de Zoom')



# TABLA 5: Grupo

class Grupo(models.Model):
    nombre = models.CharField(max_length=50)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='grupos')
    profesor = models.ForeignKey(Profesor, on_delete=models.PROTECT, related_name='grupos')
    periodo = models.CharField(max_length=20)
    cupo_maximo = models.PositiveSmallIntegerField()
    estudiantes = models.ManyToManyField(Estudiante, blank=True, related_name='grupos')
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Grupos'

    def __str__(self):
        return f"{self.nombre} - {self.materia.nombre} ({self.periodo})"



# TABLA 6: DisponibilidadProfesor

class DisponibilidadProfesor(models.Model):
    DIA_CHOICES = [
        ('LUN', 'Lunes'),
        ('MAR', 'Martes'),
        ('MIE', 'Miércoles'),
        ('JUE', 'Jueves'),
        ('VIE', 'Viernes'),
        ('SAB', 'Sábado'),
    ]

    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='disponibilidades')
    dia = models.CharField(max_length=3, choices=DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        verbose_name_plural = 'Disponibilidades'

    def __str__(self):
        return f"{self.profesor} | {self.dia}: {self.hora_inicio} - {self.hora_fin}"

    def clean(self):
        # la hora de salida tiene que ser despues de la hora de entrada
        if self.hora_inicio and self.hora_fin:
            if self.hora_fin <= self.hora_inicio:
                raise ValidationError('La hora de fin tiene que ser después de la hora de inicio')



# TABLA 7: Sesion

class Sesion(models.Model):
    TIPO_CHOICES = [
        ('CLASE', 'Clase Normal'),
        ('EXAMEN', 'Examen'),
        ('TALLER', 'Taller'),
        ('OTRO', 'Otro'),
    ]

    DIA_CHOICES = [
        ('LUN', 'Lunes'),
        ('MAR', 'Martes'),
        ('MIE', 'Miércoles'),
        ('JUE', 'Jueves'),
        ('VIE', 'Viernes'),
        ('SAB', 'Sábado'),
    ]

    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='sesiones')
    aula = models.ForeignKey(Aula, on_delete=models.PROTECT, related_name='sesiones')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='CLASE')
    dia = models.CharField(max_length=3, choices=DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    #entre que fechas aplica este horario (inicio y fin del semestre)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        verbose_name_plural = 'Sesiones'

    def __str__(self):
        return f"{self.grupo} | {self.dia} {self.hora_inicio}-{self.hora_fin} ({self.tipo})"

    def clean(self):
        #checamos que la hora de fin sea despues de la de inicio
        if self.hora_inicio and self.hora_fin:
            if self.hora_fin <= self.hora_inicio:
                raise ValidationError('La hora de fin debe ser mayor que la de inicio')

        #Aqui checamos que el aula no este ocupada ese dia y hora
        if self.aula and self.dia and self.hora_inicio and self.hora_fin:
            sesiones_en_aula = Sesion.objects.filter(
                aula=self.aula,
                dia=self.dia,
            )
            # si estamos editando, que no se compare consigo misma
            if self.pk:
                sesiones_en_aula = sesiones_en_aula.exclude(pk=self.pk)

            for s in sesiones_en_aula:
                if self.hora_inicio < s.hora_fin and self.hora_fin > s.hora_inicio:
                    raise ValidationError(f'El aula ya está ocupada de {s.hora_inicio} a {s.hora_fin}')

        # aqui checamos que el profe no este en otra clase a la misma hora
        if self.grupo and self.dia and self.hora_inicio and self.hora_fin:
            otras_clases_del_profe = Sesion.objects.filter(
                grupo__profesor=self.grupo.profesor,
                dia=self.dia,
            )
            if self.pk:
                otras_clases_del_profe = otras_clases_del_profe.exclude(pk=self.pk)

            for s in otras_clases_del_profe:
                if self.hora_inicio < s.hora_fin and self.hora_fin > s.hora_inicio:
                    raise ValidationError('El profe ya tiene otra clase a esa hora')



#TABLA 8: Asistencia

class Asistencia(models.Model):
    ESTADO_CHOICES = [
        ('PRESENTE', 'Presente'),
        ('AUSENTE', 'Ausente'),
        ('TARDANZA', 'Tardanza'),
        ('JUSTIFICADO', 'Justificado'),
    ]

    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE, related_name='asistencias')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='asistencias')
    fecha = models.DateField()
    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES)
    # si faltó, aqui se pone la razon
    observacion = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Asistencias'
        # que no se registre dos veces la asistencia del mismo alumno en la misma sesion y fecha
        constraints = [
            models.UniqueConstraint(
                fields=['estudiante', 'sesion', 'fecha'],
                name='una_asistencia_por_sesion'
            )
        ]

    def __str__(self):
        return f"{self.estudiante} | {self.fecha} -> {self.estado}"



# TABLA 9: Notificacion

class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('INFO', 'Información'),
        ('CAMBIO', 'Cambio de horario'),
        ('CANCELACION', 'Cancelación'),
        ('RECORDATORIO', 'Recordatorio'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.CharField(max_length=300)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='INFO')
    fecha = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha']  # las mas recientes primero

    def __str__(self):
        estado = '✓' if self.leida else '✗'
        return f"[{estado}] {self.usuario.username}: {self.mensaje[:50]}"
