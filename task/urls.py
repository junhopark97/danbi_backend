from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, SubTaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'subtasks', SubTaskViewSet, basename='subtask')

urlpatterns = [
    path('', include(router.urls)),
    path('tasks', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-list-create'),
    path('subtasks/<int:id>', SubTaskViewSet.as_view({'patch': 'partial_update', 'delete': 'destroy'}), name='subtask-detail'),
]
