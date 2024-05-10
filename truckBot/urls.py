from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("scrape", views.scrape, name="scrape"),
    path("send_messages", views.send_messages, name="send_messages"),
    
    # API 
    path('set_scraping_flag', views.set_scraping_flag, name='set_scraping_flag'),
    path('set_abort_flag', views.set_abort_flag, name='set_abort_flag'),

    
    path("profile/", views.profile, name="profile"),
    path("login", views.login_page, name="login"),
    path("logout", views.logout_page, name="logout"),
]