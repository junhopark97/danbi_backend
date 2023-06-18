from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from account.models import User


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField('CREATE AT', auto_now_add=True)
    modified_at = models.DateTimeField('UPDATED AT', auto_now=True)

    class Meta:
        abstract = True


class Task(TimeStampedModel):
    create_user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = ArrayField(models.CharField(max_length=50, choices=User.team_choices), default=list, blank=True, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_complete = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'task'

    def save(self, *args, **kwargs):
        # 작성자의 팀을 자동으로 추가
        if self.team is None or self.create_user.team not in self.team:
            self.team = self.team or []
            self.team.append(self.create_user.team)

        self.completed_date = timezone.now() if self.is_complete else None

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.create_user}, {self.title}'


class SubTask(TimeStampedModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    team = ArrayField(models.CharField(max_length=50, choices=User.team_choices), null=False, blank=False)
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_complete = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'subtask'

    def save(self, *args, **kwargs):
        self.completed_date = timezone.now() if self.is_complete else None

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.task.title}'
