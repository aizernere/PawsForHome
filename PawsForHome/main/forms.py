from django import forms
from .models import Account
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
 
class Create_Account(forms.Form):
    types = [
        ('shelter','I want to offer pets for adoption'),
        ('user', 'I want to adopt pets'),
    ]
    email = forms.EmailField(
        label='Enter email address',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter email address',
                'class': 'input-field',
            }))
    password = forms.CharField(
        label='Enter password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter password',
                'class': 'input-field',
            })
        )
    confirm_password = forms.CharField(
        label='Confirm your password',
        widget=forms.PasswordInput(
            attrs={
            'placeholder': 'Re-enter your password',
            'class': 'input-field',
        })
        )
    account_type = forms.ChoiceField(
        label='Account Type',
        choices=types,
        widget=forms.RadioSelect,
        )
    class Meta:
        model = Account
        fields = ['account_type', 'email', 'password']
 
    def clean_password(self):
        password = self.cleaned_data.get('password')
 
        # Use Django's built-in password validation
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(e)
 
        return password
 
    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
 
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2
 
    def save(self, commit=True):
        account = super().save(commit=False)
        account.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            account.save()
        return account
# end (gso)

class Login_Account(forms.Form):
    email = forms.CharField(label='Email Address', widget=forms.TextInput(attrs={
        'class': 'w-full p-3 border rounded-md focus:outline-none focus:border-pink-500', 
        'placeholder': 'Enter your email'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'w-full p-3 border rounded-md focus:outline-none focus:border-pink-500',
        'placeholder': 'Enter your password'
    }))
    