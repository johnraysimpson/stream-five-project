from django.contrib import admin
from .models import ParentProfile, TutorProfile, Student
# Register your models here.

class ParentProfileAdmin(admin.ModelAdmin):
    list_display=('__str__', 'first_name', 'last_name', 'telephone')
    search_fields = ('first_name', 'last_name')
    ordering = ('last_name',)
    
class TutorProfileAdmin(admin.ModelAdmin):
    list_display=('__str__', 'first_name', 'last_name', 'telephone')
    search_fields = ('first_name', 'last_name')
    ordering = ('last_name',)
    
class StudentAdmin(admin.ModelAdmin):
    list_display=('__str__', 'first_name', 'last_name', 'parent', 'relationship', 'date_of_birth')
    search_fields = ('first_name', 'last_name')
    ordering = ('last_name',)

admin.site.register(ParentProfile, ParentProfileAdmin)
admin.site.register(TutorProfile, TutorProfileAdmin)
admin.site.register(Student, StudentAdmin)