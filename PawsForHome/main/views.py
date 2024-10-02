from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import Account
from .forms import Create_Account

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def browse(request):
    return render(request, 'navbar/browse.html', {})

def notifications(request):
    return render(request, 'navbar/notifications.html', {})

def message(request):
    return render(request, 'navbar/message.html', {})

def profile(request):
    return render(request, 'navbar/profile.html', {})

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

            if confirm_password==password and not accounts.filter(email=email).exists():
                hash_password = make_password(password=password)
                create_account = Account(account_type=account_type, email=email, password=hash_password)
                create_account.save()
                return render(request,'index.html', {})
                
            elif confirm_password!=password: 
                # print("password is not the same")
                messages.warning(request, 'Passwords do not match')
            elif accounts.filter(email=email).exists():
                messages.warning(request, 'Email already exists')

    else:
        form = Create_Account()

    return render(request, 'login_signup/signup.html', {'form':form})