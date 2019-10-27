from django.urls import path, re_path
from .views import (make_payment_view,
                    get_payments_view
                    )

urlpatterns = [
    path('make_payment/<parent_id>/<student_id>/<lesson_id>', make_payment_view, name='make_payment'),
    path('my_payments/', get_payments_view, name='get_payments'),
    ]