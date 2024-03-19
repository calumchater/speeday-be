from rest_framework  import serializers

from .models import User, Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'task_name',
            'start_time',
            'end_time',
            'user_id'
        ]