# tasks/models.py
from django.db import models
from projects.models import Project
from authentication.models import CustomUser
from django.core.exceptions import ValidationError

class Task(models.Model):
    VISIBILITY_CHOICES = [('PUBLIC', 'Public'), ('PRIVATE', 'Private')]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration_days = models.IntegerField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='PUBLIC')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_tasks')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtasks')

    def save(self, *args, **kwargs):
        if self.parent_task and self.parent_task.visibility == 'PRIVATE':
            self.visibility = 'PRIVATE'
        super().save(*args, **kwargs)


class TaskDependency(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='dependencies')
    depends_on = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='dependent_on')
    condition = models.CharField(max_length=3, choices=[('AND', 'AND'), ('OR', 'OR')])

    def clean(self):
        if self.task.project != self.depends_on.project:
            raise ValidationError("Dependencies must belong to the same project.")