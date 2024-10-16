from django import forms
from .models import Pet

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'type', 'age', 'description', 'adoption_fee', 'image', 'owner']
        exclude = ['owner']