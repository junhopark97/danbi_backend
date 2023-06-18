# Generated by Django 4.2.2 on 2023-06-18 09:15

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='CREATE AT')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='UPDATED AT')),
                ('team', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('Danbi', 'Danbi'), ('Darae', 'Darae'), ('Blabla', 'Blabla'), ('Chullo', 'Chullo'), ('Ttangi', 'Ttangi'), ('Haitai', 'Haitai'), ('Sufi', 'Sufi')], max_length=50), blank=True, default=list, null=True, size=None)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('is_complete', models.BooleanField(default=False)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('create_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'task',
            },
        ),
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='CREATE AT')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='UPDATED AT')),
                ('team', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('Danbi', 'Danbi'), ('Darae', 'Darae'), ('Blabla', 'Blabla'), ('Chullo', 'Chullo'), ('Ttangi', 'Ttangi'), ('Haitai', 'Haitai'), ('Sufi', 'Sufi')], max_length=50), size=None)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('is_complete', models.BooleanField(default=False)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtasks', to='task.task')),
            ],
            options={
                'db_table': 'subtask',
            },
        ),
    ]
