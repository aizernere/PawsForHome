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

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if any(char.isdigit() for char in name):
            raise forms.ValidationError("Name should not contain numbers.")
        return name

    def clean_age_years(self):
        age_years = self.cleaned_data.get('age_years')
        if age_years and (age_years < 0 or age_years > 100):
            raise forms.ValidationError("Is your pet older than a turtle? Please contact your system administrator.")
        return age_years

    def clean_age_months(self):
        age_months = self.cleaned_data.get('age_months')
        if age_months and (age_months < 0 or age_months > 11):
            raise forms.ValidationError("Months must be between 0-11.")
        return age_months

    def clean_adoption_fee(self):
        adoption_fee = self.cleaned_data.get('adoption_fee')
        if adoption_fee in [None, '']:
            adoption_fee = 0
        if adoption_fee and len(str(adoption_fee)) >= 8:
            raise forms.ValidationError("Adoption fee must be less than 8 digits.")
        return adoption_fee

    def clean(self):
        cleaned_data = super().clean()
        image = self.files.get('image') 
        if not image:
            self.add_error('image', "A valid image must be uploaded.")
        return cleaned_data