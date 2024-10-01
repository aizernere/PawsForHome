from django.shortcuts import render
# from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import Account
from .forms import Create_Account

# Create your views here.
def create_account(request):
    accounts = Account.objects.all()

    if request.method == 'POST':
        form = Create_Account(request.POST)

        if form.is_valid():

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')
            account_type = form.cleaned_data.get('account_type')
            print(f'{email} {password} {confirm_password} {account_type}')        

            if confirm_password==password and not Account.objects.filter(email=email).exists():
                hash_password = make_password(password=password)
                create_account = Account(account_type=account_type, email=email, password=hash_password)
                create_account.save()
                
            else: 
                print("password is not the same")
    else:
        form = Create_Account()

    return render(request, 'login_signup/signup.html', {'form':form})