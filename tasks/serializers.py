from rest_framework import serializers
from .models import Task, TaskDependency
from authentication.models import CustomUser
from authentication.serializers import UserSerializer

class TaskDependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDependency
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    dependencies = TaskDependencySerializer(many=True, read_only=True)
    assigned_to = UserSerializer(read_only=True)  # Read-only for GET requests
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='assigned_to', write_only=True
    ) 

    class Meta:
        model = Task
        fields = '__all__'