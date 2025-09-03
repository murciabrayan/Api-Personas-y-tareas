from django.contrib import admin
from django.urls import path
from api_project.api_app import views
from api_project.api_app import views

urlpatterns = [
    # Tareas
path('api/tareas/', views.TareaListCreate.as_view(), name='tarea-list'),
path('api/tareas/actualizar/<int:pk>/', views.ActualizarTarea.as_view(), name='tarea-actualizar'),
path('api/tareas/eliminar/<int:pk>/', views.EliminarTarea.as_view(), name='tarea-eliminar'),
path('api/tareas/fecha/<str:fecha>/', views.TareasPorFecha.as_view(), name='tarea-fecha'),
path('api/tareas/rango/<str:fecha_inicio>/<str:fecha_fin>/', views.TareasPorRangoFechas.as_view(), name='tarea-rango'),
path('api/tareas/persona/<str:documento>/', views.TareasPorDocumentoPersona.as_view(), name='tarea-por-persona'),

#inicio

    path('admin/', admin.site.urls),
path('', views.index, name='index'),

    # Personas
    path('api/personas/', views.Personalist.as_view(), name='persona-list'),
    path('api/personas/crear/', views.CrearPersona.as_view(), name='persona-crear'),
    path('api/personas/actualizar/<int:pk>/', views.ActualizarPersona.as_view(), name='persona-actualizar'),
    path('api/personas/documento/<str:documento>/', views.PersonaByDocumento.as_view(), name='persona-documento'),
]
