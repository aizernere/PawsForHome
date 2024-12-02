from django import forms
from .models import Pet

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'type', 'age_years', 'age_months','description', 'adoption_fee', 'image', 'owner', 'location', 'breed']
        exclude = ['owner', 'location']
    
    type = forms.ChoiceField(
        choices=Pet.TYPE_CHOICES,  
        widget=forms.RadioSelect,   
        required=True,              
    )