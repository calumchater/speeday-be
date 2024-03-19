from django.test import TestCase
import pytest

from ..models import Task

# Create your tests here.
TEST_SIZE = 10000


@pytest.fixture
def project():
    return Task.objects.create(
        task_name="Test",
        start_time="2021-12-12 00:00:00",
        end_time="2021-12-13 00:00:00",
    )


# class TestTask:
#     def test_create_task(self, client, project):
#         test_url = reverse(
#             "project-task-list-create-update",
#             kwargs={
#                 "project_id": project.id,
#             },
#         )

#         for x in range(TEST_SIZE):
#             # test auto setting sequence
#             response = client.post(
#                 test_url, data={"name": "Test_{}".format(x), "description": "test"}
#             )
#             assert response.status_code == status.HTTP_201_CREATED
