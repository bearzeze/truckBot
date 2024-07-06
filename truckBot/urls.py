from django.urls import path

from . import views

urlpatterns = [
    # Home page
    path('', views.index, name="index"),
    path('scrape', views.scrape, name="scrape"),
    path('send_messages', views.send_messages, name="send_messages"),
    path('prepare_loads/<str:company>', views.prepare_loads, name="prepare_loads"),
    
    
    # API 
    path('api/set_scraping_flag', views.set_scraping_flag, name="set_scraping_flag"),
    path('api/set_abort_flag', views.set_abort_flag, name="set_abort_flag"),
    path('api/change_message/<int:load_id>', views.change_load_message, name="change_load_message"),
    path('api/load_history', views.load_history, name="load_history"),
    path('api/open_txt_file/<str:company>', views.open_txt_file, name="open_txt_file"),
    path('api/clear_txt_file/<str:company>', views.clear_txt_file, name="clear_txt_file"),

    
    # Profile page
    path('profile/', views.profile, name="profile"),
    path('login', views.login_page, name="login"),
    path('logout', views.logout_page, name="logout"),
    
    path('<str:everything_else>', views.no_page, name="no_page")
]