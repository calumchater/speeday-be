from django.http import JsonResponse, HttpResponse

from rest_framework import authentication, generics, mixins, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.authentication import TokenAuthentication

from speeday_app.models import Task
from speeday_app.serializers import TaskSerializer

@api_view(['GET'])
def home(request, *args, **kwargs):
    return JsonResponse({'message': 'Hello, world!'})


# @api_view(['POST'])
class TaskListCreateAPIView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def perform_create(self, serializer):
        task_name = serializer.validated_data.get('task_name')
        start_time = serializer.validated_data.get('start_time')
        end_time = serializer.validated_data.get('end_time')
        user_id = serializer.validated_data.get('user_id')
        serializer.save(task_name=task_name, start_time=start_time, end_time=end_time, user_id=2)
            # return Response(serializer.data, status=HttpResponse.HTTP_201_CREATED)
