from django.urls import path
from .views import search_parent

urlpatterns = [
    path('parent/search', search_parent, name="search-parent")
    ]