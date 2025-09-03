from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Persona
from .serializers import PersonaSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from django.db.models import Q
from datetime import datetime

from .models import Persona, Tarea
from .serializers import PersonaSerializer, TareaSerializer


# Listar y crear personas
class Personalist(generics.ListCreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

    def get(self, request):
        personas = Persona.objects.all()
        serializer = PersonaSerializer(personas, many=True)
        if not personas:
            raise NotFound('No se encontraron personas.')
        return Response({'success': True, 'detail': 'Listado de personas.', 'data': serializer.data}, status=status.HTTP_200_OK)

# Actualizar persona
class ActualizarPersona(generics.UpdateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

    def put(self, request, pk):
        persona = get_object_or_404(Persona, pk=pk)
        email = request.data.get('email', None)

        # Verificar si el email ha cambiado
        if email and email != persona.email:
            # Verificar si ya existe otra persona con el mismo email
            if Persona.objects.filter(email=email).exclude(pk=pk).exists():
                return Response({'email': ['Persona with this email already exists.']}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PersonaSerializer(persona, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'detail': 'Persona actualizada correctamente.', 'data': serializer.data}, status=status.HTTP_200_OK)

# Buscar persona por documento
class PersonaByDocumento(generics.ListAPIView):
    serializer_class = PersonaSerializer

    def get(self, request, documento):
        persona = Persona.objects.filter(documento=documento).first()
        if not persona:
            raise NotFound('No se encontró una persona con ese documento.')
        serializer = PersonaSerializer(persona)
        return Response({'success': True, 'detail': 'Persona encontrada.', 'data': serializer.data}, status=status.HTTP_200_OK)

# Crear personas
class CrearPersona(generics.CreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

    def post(self, request):
        serializer = PersonaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'detail': 'Persona creada correctamente.', 'data': serializer.data}, status=status.HTTP_201_CREATED)


# Listar y crear tareas
class TareaListCreate(generics.ListCreateAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

    def get(self, request):
        tareas = Tarea.objects.all()
        serializer = TareaSerializer(tareas, many=True)
        if not tareas:
            raise NotFound("No se encontraron tareas.")
        return Response({"success": True, "detail": "Listado de tareas.", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TareaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, "detail": "Tarea creada correctamente.", "data": serializer.data}, status=status.HTTP_201_CREATED)


# Actualizar tarea
class ActualizarTarea(generics.UpdateAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

    def put(self, request, pk):
        tarea = get_object_or_404(Tarea, pk=pk)
        serializer = TareaSerializer(tarea, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, "detail": "Tarea actualizada correctamente.", "data": serializer.data}, status=status.HTTP_200_OK)


# Eliminar tarea
class EliminarTarea(generics.DestroyAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

    def delete(self, request, pk):
        tarea = get_object_or_404(Tarea, pk=pk)
        tarea.delete()
        return Response({"success": True, "detail": "Tarea eliminada correctamente."}, status=status.HTTP_204_NO_CONTENT)

# Filtrar tareas por fecha límite exacta
class TareasPorFecha(generics.ListAPIView):
    serializer_class = TareaSerializer

    def get(self, request, fecha):
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            return Response({"success": False, "detail": "Formato de fecha inválido. Usa YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        tareas = Tarea.objects.filter(fecha_limite=fecha_obj)
        serializer = TareaSerializer(tareas, many=True)
        if not tareas:
            raise NotFound("No se encontraron tareas para esa fecha.")
        return Response({"success": True, "detail": "Tareas filtradas por fecha.", "data": serializer.data}, status=status.HTTP_200_OK)


# Filtrar tareas por rango de fechas
class TareasPorRangoFechas(generics.ListAPIView):
    serializer_class = TareaSerializer

    def get(self, request, fecha_inicio, fecha_fin):
        try:
            inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        except ValueError:
            return Response({"success": False, "detail": "Formato de fecha inválido. Usa YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        tareas = Tarea.objects.filter(fecha_limite__range=(inicio, fin))
        serializer = TareaSerializer(tareas, many=True)
        if not tareas:
            raise NotFound("No se encontraron tareas en ese rango de fechas.")
        return Response({"success": True, "detail": "Tareas filtradas por rango de fechas.", "data": serializer.data}, status=status.HTTP_200_OK)


# Filtrar tareas por documento de persona
class TareasPorDocumentoPersona(generics.ListAPIView):
    serializer_class = TareaSerializer

    def get(self, request, documento):
        persona = Persona.objects.filter(documento=documento).first()
        if not persona:
            raise NotFound("No se encontró una persona con ese documento.")
        tareas = Tarea.objects.filter(persona=persona)
        serializer = TareaSerializer(tareas, many=True)
        if not tareas:
            raise NotFound("La persona no tiene tareas registradas.")
        return Response({"success": True, "detail": "Tareas filtradas por documento de persona.", "data": serializer.data}, status=status.HTTP_200_OK)


def index(request):
    data = {
        "message": "Bienvenido a la API de Personas y Tareas",
        "endpoints": {
            "listar_personas": "/api/personas/",
            "crear_persona": "/api/personas/crear/",
            "actualizar_persona": "/api/personas/actualizar/<id>/",
            "buscar_por_documento": "/api/personas/documento/<documento>/"
        }
    }
    # Evitamos que Django escape caracteres especiales como < >
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
