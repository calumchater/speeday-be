from rest_framework  import serializers

from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'task_name',
            'start_time',
            'end_time',
            'user_id'
        ]