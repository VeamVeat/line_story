from django.urls import path
from users.views import ProfileView

app_name = "users"


urlpatterns = [
    path("profile/<int:pk>", ProfileView.as_view(), name="profile")
]
