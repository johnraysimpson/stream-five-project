from django.contrib import admin
from .models import ParentProfile, TutorProfile, TutorSession, Student
# Register your models here.

admin.site.register(ParentProfile)
admin.site.register(TutorProfile)
admin.site.register(TutorSession)
admin.site.register(Student)