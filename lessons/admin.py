from django.contrib import admin
from .models import TutorSession, StudentSession

class TutorSessionAdmin(admin.ModelAdmin):
    list_display=('tutor', 'centre', 'subject', 'day', 'time', 'date',)


admin.site.register(TutorSession, TutorSessionAdmin)
admin.site.register(StudentSession)