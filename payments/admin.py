from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display=('first_name', 'last_name', 'student_first_name', 'student_last_name', 'subject', 'centre_name', 'date', 'amount_paid', 'date_paid')
    search_fields = ('first_name', 'last_name')
    ordering = ('-date_paid',)

# Register your models here.
admin.site.register(Payment, PaymentAdmin)