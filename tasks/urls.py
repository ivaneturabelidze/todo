from django.urls import path
from .views import tasks_view, task_view

urlpatterns = [
    path("tasks/", tasks_view),
    path("tasks/<int:task_id>", task_view)
]
