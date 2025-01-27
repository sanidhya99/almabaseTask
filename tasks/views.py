from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .models import Task
from django.shortcuts import get_object_or_404
from .serializers import TaskSerializer, TaskDependencySerializer


class TaskListView(generics.ListAPIView):
    
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user).order_by('start_date')


class TaskUpdateView(generics.UpdateAPIView):
   
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        task = self.get_object()
        if task.created_by != self.request.user:
            raise PermissionError("Only the task creator can update this task.")
        serializer.save()


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(Q(assigned_to=user) | Q(project__created_by=user)).distinct()


class TaskCompleteView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        if task.assigned_to != request.user and task.project.created_by != request.user:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

        task.is_completed = True
        task.save()
        # Check and mark parent task as completed
        if task.parent_task and all(sub.is_completed for sub in task.parent_task.subtasks.all()):
            task.parent_task.is_completed = True
            task.parent_task.save()
        return Response({"detail": "Task marked as complete."})
    


class TaskDependencyCreateView(generics.CreateAPIView):
    serializer_class = TaskDependencySerializer

    def perform_create(self, serializer):
        task = serializer.validated_data['task']
        depends_on = serializer.validated_data['depends_on']
        condition = serializer.validated_data.get('condition', 'AND')
        if task.project != depends_on.project:
            return Response({"error": "Tasks must belong to the same project."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

class TaskDependencyCheckView(generics.GenericAPIView):
    serializer_class = TaskSerializer

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs['pk'])
        dependencies = task.dependencies.all()
        response = {"task": task.title, "can_start": True, "details": []}

        for dependency in dependencies:
            if dependency.condition == 'AND':
                can_start = dependency.depends_on.is_completed
            elif dependency.condition == 'OR':
                can_start = any(dep.depends_on.is_completed for dep in dependencies)

            response["details"].append({
                "depends_on": dependency.depends_on.title,
                "is_completed": dependency.depends_on.is_completed,
                "condition": dependency.condition,
                "can_start": can_start
            })

        response["can_start"] = all(detail["can_start"] for detail in response["details"])
        return Response(response)