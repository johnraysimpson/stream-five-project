from django.contrib import admin
from .models import Lesson

class LessonAdmin(admin.ModelAdmin):
    def date_format(self, obj):
        return obj.date.strftime("%d/%m/%Y")   
    date_format.admin_order_field = 'date'
    
    list_display=('tutor', 'centre', 'subject', 'day', 'time', 'date_format')
    ordering = ('date', )


admin.site.register(Lesson, LessonAdmin)