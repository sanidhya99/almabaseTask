from django.urls import path
from .views import TaskListCreateView, TaskCompleteView, TaskDependencyCreateView, TaskDependencyCheckView, TaskListView, TaskUpdateView

urlpatterns = [
    path('self/tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/complete/', TaskCompleteView.as_view(), name='task-complete'),
    path('dependencies/', TaskDependencyCreateView.as_view(), name='dependency-create'),
    path('tasks/<int:pk>/check/', TaskDependencyCheckView.as_view(), name='dependency-check'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
]