from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("scrape", views.scrape, name="scrape"),
    
    path("profile/", views.profile, name="profile"),
    path("login", views.login_page, name="login"),
    path("logout", views.logout_page, name="logout"),
]