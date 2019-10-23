from django.contrib import admin
from .models import Lesson

class LessonAdmin(admin.ModelAdmin):
    list_display=('tutor', 'centre', 'subject', 'day', 'time', 'date',)


admin.site.register(Lesson, LessonAdmin)