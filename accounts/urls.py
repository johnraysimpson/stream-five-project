from django.urls import path, include
from . import urls_reset
from .views import login_view, logout, first_password_change
from django.contrib.auth.views import password_change, password_change_done


urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout/', logout, name="logout"),
    path('password-reset/', include(urls_reset)),
    path('change-password/', password_change, name='password_change'),
    path('change-password-done/', password_change_done, name="password_change_done"),
    path('first-password-change/', first_password_change, name="first_password_change")
    ]