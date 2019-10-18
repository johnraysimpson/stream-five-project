from django.contrib import admin
from .models import ParentProfile, TutorProfile, TutorSession
# Register your models here.

admin.site.register(ParentProfile)
admin.site.register(TutorProfile)
admin.site.register(TutorSession)