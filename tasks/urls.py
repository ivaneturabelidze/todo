from django.urls import path
from .views import tasks_view

urlpatterns = [
    path("tasks/", tasks_view),
]
