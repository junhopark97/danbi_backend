from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put']

    def get_queryset(self):
        user_team = self.request.user.team
        query = Task.objects.filter(
            Q(subtasks__team__contains=[user_team]) |
            Q(team__contains=[user_team])
        ).distinct().order_by('-created_at')
        return query

    def update(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()

        if user != instance.create_user:
            raise PermissionDenied('You do not have permission to edit this Task.')
        super().update(request, *args, **kwargs)

        return Response(
            {
                'message': 'Task modification succeeded.'
            },
            status=status.HTTP_200_OK
        )


class SubTaskViewSet(viewsets.ModelViewSet):
    serializer_class = SubTaskSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('patch', 'delete',)
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return SubTask.objects.filter(
            Q(team__contains=[user.team])).order_by('-created_at')

    def partial_update(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()

        if user.team in instance.team:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            task = get_object_or_404(Task, id=instance.task_id)
            all_subtasks_complete = task.subtasks.filter(is_complete=False).exists()

            if not all_subtasks_complete:
                task.is_complete = True
            else:
                task.is_complete = False
            task.save()

            return Response(
                {
                    'message': 'Subtask updated successfully.'
                },
                status=status.HTTP_200_OK
            )
        else:
            raise PermissionDenied('You do not have permission to update this SubTask.')

    def destroy(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()

        if instance.is_complete:
            raise PermissionDenied('Completed subtasks cannot be deleted.')

        task = get_object_or_404(Task, id=instance.task_id)

        if user != task.create_user:
            raise PermissionDenied('You do not have permission to delete this SubTask.')

        try:
            super().destroy(request, *args, **kwargs)
        except Http404:
            raise Http404('SubTask not found.')

        return Response(
            {
                'message': 'Subtask has been deleted.'
            },
            status=status.HTTP_204_NO_CONTENT,
        )
