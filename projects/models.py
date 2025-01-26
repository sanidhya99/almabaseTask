# projects/models.py
from django.db import models
from auth.models import User

class Project(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    collaborators = models.ManyToManyField(User, related_name='collaborating_projects')

    def __str__(self):
        return self.title
