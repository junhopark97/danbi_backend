from rest_framework import serializers
from .models import Task, SubTask


class SubTaskSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate_team(self, value):
        if not value:
            raise serializers.ValidationError('A value is required for the team field.')

        teams = ('Danbi', 'Darae', 'Blabla', 'Chullo', 'Ttangi', 'Haitai', 'Sufi')
        for team in value:
            if team not in teams:
                raise serializers.ValidationError(f'Team "{team}" is not a valid choice.')
        return value

    class Meta:
        model = SubTask
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, required=False)
    create_user = serializers.StringRelatedField(read_only=True)
    is_complete = serializers.BooleanField(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks')
        task = Task.objects.create(create_user=self.context['request'].user, **validated_data)
        for subtask_data in subtasks_data:
            SubTask.objects.create(task=task, **subtask_data)
        return task

    def update_subtasks(self, instance, subtasks_data):
        for subtask_data in subtasks_data:
            subtask_id = subtask_data.get('id')
            if subtask_id:
                subtask = SubTask.objects.get(id=subtask_id, task=instance)
                for attr, value in subtask_data.items():
                    setattr(subtask, attr, value)
                subtask.save()

    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks')
        if subtasks_data:
            self.update_subtasks(instance, subtasks_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
