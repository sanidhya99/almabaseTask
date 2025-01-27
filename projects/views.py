from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q
from collections import defaultdict, deque
from .models import Project
from .serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticated
from projects.utils import calculate_schedule
from tasks.models import Task
from tasks.serializers import TaskSerializer


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(Q(created_by=user) | Q(collaborators=user)).distinct()

    def perform_create(self, serializer):
        serializer.save()



class ProjectScheduleView(generics.RetrieveAPIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            project = Project.objects.get(id=pk)
            tasks = Task.objects.filter(project=project, is_completed=False).select_related('assigned_to')
            collaborators = tasks.values_list('assigned_to', flat=True).distinct()
            
            # Calculate schedules
            schedules = calculate_schedule(tasks, collaborators)

            # Serialize response
            serialized_data = {}
            for user, tasks in schedules.items():
                serialized_data[user] = TaskSerializer(tasks, many=True).data

            return Response(serialized_data, status=200)
        except Project.DoesNotExist:
            return Response({"error": "Project not found."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

