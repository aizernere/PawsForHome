from django import forms 
from .models import Account

class Create_Account(forms.Form):
    types = [
        ('shelter','Shelter'),
        ('user', 'User'),
    ]

    email = forms.CharField(label='Enter email address')
    password = forms.CharField(
        label='Enter password',
        widget=forms.PasswordInput
        )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput
        )
    account_type = forms.ChoiceField(
        label='Account Type',
        widget=forms.RadioSelect,
        choices=types
        )
    
    class Meta:
        model = Account
        fields = ['account_type', 'email', 'password']

    # gikan stack overflow
        def clean_password2(self):
            password1 = self.cleaned_data.get('password')
            password2 = self.cleaned_data.get('confirm_password')

            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Passwords do not match")
            return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
# end (gso)