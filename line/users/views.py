from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse

from users.forms import RegisterUserForm


def home(request):
    return render(request, "users/dashboard.html")


def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": RegisterUserForm}
        )
    elif request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("home"))
