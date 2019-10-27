from django.urls import path, re_path
from .views import (tutoruser_earnings_view
                    )

urlpatterns = [
    re_path(r'^my_earnings/(?P<request_date>\d{4}-\d{2}-\d{2})$', tutoruser_earnings_view, name='my_earnings'),
    ]