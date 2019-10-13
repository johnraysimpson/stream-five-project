from django.urls import path, include
from . import urls_reset
from .views import login_view, logout


urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout/', logout, name="logout"),
    path('password-reset/', include(urls_reset))
    ]