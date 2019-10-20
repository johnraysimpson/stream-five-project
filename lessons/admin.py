from django.contrib import admin
from .models import TutorSession, StudentSession

# Register your models here.
admin.site.register(TutorSession)
admin.site.register(StudentSession)