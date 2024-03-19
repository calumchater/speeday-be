from rest_framework import generics

from rest_framework.response import Response

from speeday_app.models import Task
from speeday_app.serializers import TaskSerializer

from google_client.calendar_service import GoogleCalendarService


class TaskListCreateAPIView(generics.CreateAPIView, request):
    
    serializer_class = TaskSerializer

    def perform_create(self, serializer):

        breakpoint() 

        task_name = serializer.validated_data.get("task_name")
        start_time = serializer.validated_data.get("start_time")
        end_time = serializer.validated_data.get("end_time")
        # user

        access_token = self.request.access_token

        # Create the event in the cale ndar
        GoogleCalendarService(access_token).create_event(
            {"task_name": "suck_it", "start_time": "10:15", "end_time": "10:40"}
        )

        serializer.save(
            task_name=task_name, start_time=start_time, end_time=end_time, user_id=1
        )
