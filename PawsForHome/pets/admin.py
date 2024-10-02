from django.contrib import admin
from .models import Pet

class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'age', 'adoption_fee', 'status', 'created_at')

# Register with custom display
admin.site.register(Pet, PetAdmin)