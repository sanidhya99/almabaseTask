from django.urls import path
from .views import *

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/schedule/', ProjectScheduleView.as_view(), name='project-schedule'),
]