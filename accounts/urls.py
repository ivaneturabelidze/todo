from django.urls import path
from .views import users_view, user_details

urlpatterns = [
    path("users/", users_view),
    path("users/<int:user_id>", user_details),
]
