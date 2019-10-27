from django.urls import path
from .views import (
                    get_tutor_lessons_view,
                    )

urlpatterns = [
        path('view_lessons/', get_tutor_lessons_view, name="get_tutor_lessons"),
    ]