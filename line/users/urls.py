from django.urls import path
from users.views import ProfileView, ProfileUpdateView

app_name = "users"


urlpatterns = [
    path("profile_update/<int:id>", ProfileUpdateView.as_view(), name="profile_update"),
    path("profile/<int:pk>", ProfileView.as_view(), name="profile")
]
