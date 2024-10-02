from django.contrib import admin
from .models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'account_type', 'is_active', 'is_staff')

# Register your models here.
admin.site.register(Account, AccountAdmin)