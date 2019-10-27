from django.urls import path
from .views import (
                    get_tutoruser_profile
                    )

urlpatterns = [
        path('my_profile/', get_tutoruser_profile, name="tutor_profile"),
    ]