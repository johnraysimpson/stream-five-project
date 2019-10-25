from django.urls import path, re_path
from .views import (tutor_earnings_view,
                    payments_view
                    )

urlpatterns = [
    #path('tutor_earnings/<tutor_id>/', tutor_earnings_view, name="tutor_earnings"),
    path('payments/', payments_view, name="payments"),
    re_path(r'^tutor_earnings/(?P<tutor_id>\d+)/(?P<request_date>\d{4}-\d{2}-\d{2})$', tutor_earnings_view, name='tutor_earnings'),
    ]