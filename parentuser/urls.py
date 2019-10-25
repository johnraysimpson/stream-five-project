from django.urls import path
from .views import (
                    parent_dashboard_view,
    )

app_name = 'parentuser'
urlpatterns = [
        path('', parent_dashboard_view),
        path('dashbaord/', parent_dashboard_view, name="dashboard")
    ]