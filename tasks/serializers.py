from rest_framework import serializers
from .models import Task, TaskDependency

class TaskDependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDependency
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    dependencies = TaskDependencySerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'