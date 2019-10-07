from django.urls import path
from .views import home_view, about_view, contact_view, login_view, logout

urlpatterns = [
    path('', home_view),
    path('home/', home_view, name="home"),
    path('about/', about_view, name="about"),
    path('contact/', contact_view, name="contact"),
    path('login/', login_view, name="login"),
    path('logout/', logout, name="logout")
    ]