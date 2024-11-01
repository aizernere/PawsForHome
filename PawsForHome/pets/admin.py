from django.contrib import admin
from .models import Pet, AdoptionRequest, Favorite

class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'age_years', 'age_months','adoption_fee', 'status', 'created_at')

# Register with custom display
admin.site.register(Pet, PetAdmin)
admin.site.register(AdoptionRequest)
admin.site.register(Favorite)