from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from account.models import User
from task.models import Task, SubTask
from django.db import models
from django import forms


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('create_user', 'team', 'title', 'short_content',)
    list_display_links = ('create_user',)

    def short_content(self, task):
        return task.content[:10]


class SubTaskAdminForm(forms.ModelForm):
    team = forms.MultipleChoiceField(choices=User.team_choices, widget=forms.SelectMultiple)

    class Meta:
        model = SubTask
        fields = '__all__'


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'team',)
    list_display_links = ('team',)

    form = SubTaskAdminForm

# admin.site.register(SubTask, SubTaskAdmin)
