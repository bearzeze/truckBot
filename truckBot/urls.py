from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_page, name="login"),
    path("logout", views.logout_page, name="logout"),

    path("profile/", views.profile, name="profile"),
]