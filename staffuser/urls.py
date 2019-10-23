from django.urls import path, re_path, include
from .views import (staff_dashboard_view,
                    parents_view,
                    )
from profiles import urls as profile_urls
from lessons import urls as lesson_urls
from accounts import urls_create as create_user_urls
from search import urls as search_urls

app_name = 'staffuser'
urlpatterns = [
    path('', staff_dashboard_view),
    path('', include(profile_urls)),
    path('', include(lesson_urls)),
    path('', include(create_user_urls)),
    path('dashboard/', staff_dashboard_view, name="dashboard"),
    path('parent/', parents_view, name='parents'),
    path('', include(search_urls)),
    ]