from django.urls import path, include
from . import urls_reset
from .views import login_view, logout, first_password_change
from django.contrib.auth.views import password_change, password_change_done


urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout/', logout, name="logout"),
    path('password_reset/', include(urls_reset)),
    path('change_password/', password_change, name='password_change'),
    path('change_password_done/', password_change_done, name="password_change_done"),
    path('first_password_change/', first_password_change, name="first_password_change")
    ]