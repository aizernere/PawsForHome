from django import forms
from .models import Account
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from pets.models import AdoptionRequest
 
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
    
class Profile_Filling(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={
            'class': 'input-field',
            'placeholder': 'Enter your first name',
            }
        )
    )
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(
            attrs={
            'class': 'input-field',
            'placeholder': 'Enter your last name',
            }
        )
    )
    birthdate = forms.DateField(
        label='Birthdate',
        widget=forms.DateInput(
            attrs={
                'class': 'input-field',
                'type': 'date',
                'placeholder': 'Enter your birthdate',
            }
        )
    )
    phone_number = forms.CharField(
        label='Phone Number',
        widget=forms.NumberInput(
            attrs={
                'class': 'input-field',
                'placeholder': 'Enter your phone number',
            }
        ),
        max_length=11 
    )
    address = forms.CharField(
        label='Address',
        widget=forms.Textarea(
            attrs={
                'class': 'input-field',
                'placeholder': 'Enter your address',
                'rows': 3, 
            }
        ),
        required=True
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and len(str(phone_number)) != 11:
            raise forms.ValidationError("Phone number must be exactly 11 digits.")
        return phone_number

class AdoptionForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 'address',
            'housing_type', 'household_description', 'general_info',
            'other_housing_description', 'other_general_info',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Phone Number'}), 
            'address': forms.Textarea(attrs={'class': 'input-field', 'placeholder': 'Address'}),
            'housing_type': forms.RadioSelect(),  
            'household_description': forms.RadioSelect(),  
            'general_info': forms.RadioSelect(), 
            'other_housing_description': forms.Textarea(attrs={'class': 'input-field', 'placeholder': 'If Other, describe here', 'rows': 3}),
            'other_general_info': forms.Textarea(attrs={'class': 'input-field', 'placeholder': 'If Other, describe here', 'rows': 3}),
        }