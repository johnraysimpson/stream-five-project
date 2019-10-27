from django.urls import path, re_path, include
from .views import (
                    tutor_dashboard_view,
    )
from profiles import tutor_urls as profile_urls
from payments import tutor_urls as payment_urls

app_name = 'tutoruser'
urlpatterns = [
        path('', tutor_dashboard_view),
        path('dashboard/', tutor_dashboard_view, name="dashboard"),
        path('', include(profile_urls)),
        path('', include(payment_urls)),
    ]