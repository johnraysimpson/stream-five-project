from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User

class UserAdmin(BaseUserAdmin):
    """Forms for adding and changing a user within the admin panel"""
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email', 'admin','staff', 'active', 'parent', 'tutor', 'password_changed', 'centre')
    list_filter = ('admin','staff', 'active', 'parent', 'tutor')
    fieldsets = (
        (None, {'fields': ('email', 'password','password_changed', 'centre')}),
        ('Permissions', {'fields': ('admin','staff', 'active', 'parent', 'tutor', 'password_changed')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'admin','staff', 'active', 'parent', 'tutor', 'centre', 'password_changed')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)



# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)