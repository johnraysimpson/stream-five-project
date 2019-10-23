from django.urls import path
from .views import add_parent_view, add_tutor_view


urlpatterns = [
    path('addparent/', add_parent_view, name="add-parent"),
    path('addtutor/', add_tutor_view, name="add-tutor"),
    ]