from django.urls import path, include
from .views import (
                    parent_dashboard_view,
    )
from lessons import parent_urls as lesson_urls
from profiles import parent_urls as profile_urls
from payments import parent_urls as payment_urls

app_name = 'parentuser'
urlpatterns = [
        path('', parent_dashboard_view),
        path('dashbaord/', parent_dashboard_view, name="dashboard"),
        path('', include(lesson_urls)),
        path('', include(profile_urls)),
        path('', include(payment_urls)),
    ]