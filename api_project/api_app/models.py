from django.db import models

class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True, editable=False, db_column='T001IdPersona')
    nombre = models.CharField(max_length=100, db_column='T001Nombre')
    apellido = models.CharField(max_length=100, db_column='T001Apellido')
    documento = models.CharField(max_length=20, unique=True, db_column='T001Documento')
    email = models.EmailField(unique=True, db_column='T001Email')
    activo = models.BooleanField(default=True, db_column='T001Activo')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        db_table = 'T001Persona'
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'

class Tarea(models.Model):
    id_tarea = models.AutoField(primary_key=True, editable=False, db_column='T002IdTarea')
    titulo = models.CharField(max_length=200, db_column='T002Titulo')
    descripcion = models.TextField(db_column='T002Descripcion')
    fecha_limite = models.DateField(db_column='T002Fechalimite')
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='tareas', db_column='T002PersonaId')

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'T002Tarea'
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'        