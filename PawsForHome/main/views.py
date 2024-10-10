from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import Account
from .forms import Create_Account, Login_Account
from django.contrib.auth import login, authenticate, logout

# Create your views here.

def landing_page(request):
     return render(request, 'landing_page.html', {})
def index(request):
    return render(request, 'index.html', {})
def adoptionform(request):
    return render(request, 'adoptionform.html', {})
def shelterdashboard(request):
    return render(request, 'shelterdashboard.html', {})
def notifications(request):
    return render(request, 'navbar/notifications.html', {})

def message(request):
    return render(request, 'navbar/message.html', {})

def profile(request):
    return render(request, 'navbar/profile.html', {})

def home(request):
    return render(request, 'home.html', {})

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
                # return render(request,'index.html', {})
                return redirect('main:login_account')
                
            elif confirm_password!=password: 
                # print("password is not the same")
                messages.warning(request, 'Passwords do not match')
            elif accounts.filter(email=email).exists():
                messages.warning(request, 'Email already exists')

    else:
        form = Create_Account()

    return render(request, 'login_signup/signup.html', {'form':form})

def login_account(request):
    if request.method == 'POST':
        form = Login_Account(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            # if Account.objects.filter(email=email).exists():
            #     login_account = Account.objects.get(email=email)
            #     if login_account.check_password(password):  
            #         login(request, login_account)  
            #         return redirect('main:home')  
            #     else:
            #         error_message = "Invalid password."
            # else:
            #     error_message = "Account with this email does not exist."
            if user:
                login(request, user)
                return redirect('main:home')
        error_message = "Invalid email or password."
        return render(request, 'login_signup/login.html', {'form': form, 'error_message': error_message})

    else:  
        form = Login_Account()
        return render(request, 'login_signup/login.html', {'form': form})
    
def logout_account(request):
    logout(request)
    return redirect('main:landing_page')