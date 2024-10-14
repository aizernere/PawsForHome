from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import Account
from .forms import Create_Account, Login_Account, Profile_Fillling
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
def user_dashboard(request):
    return render(request, 'userdashboard.html', {})
def pet_listings(request):
    return render(request, 'shelterdashboard/pet_listings.html',{})
def adoptform(request):
    return render(request, 'shelterdashboard/adoptform.html',{})
def pending_requests(request):
    return render(request, 'shelterdashboard/pending_requests.html',{})
def notifications(request):
    return render(request, 'navbar/notifications.html', {})

def message(request):
    return render(request, 'navbar/message.html', {})

def profile(request):
    return render(request, 'navbar/profile.html', {})

def home(request):
    return render(request, 'home.html', {})

def profile_filling_page(request):
    # accounts = Account.objects.all()
    curr_account = Account.objects.last()

    if request.method == 'POST':
        form = Profile_Fillling(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            birthdate = form.cleaned_data.get('birthdate')
            phone_num = form.cleaned_data.get('phone_number')

            if phone_num and first_name and last_name and birthdate:
                phone_len = len(str(phone_num))
                if phone_len != 10:
                    messages.warning(request, 'Input 11 digit number')
                else: 
                    curr_account.first_name = first_name
                    curr_account.last_name = last_name
                    curr_account.birth_date = birthdate
                    curr_account.phone_number = phone_num

                    curr_account.save()

                    return redirect('main:login_account')
        else:
            messages.warning(request, 'All fields are required')

    else:
        form = Profile_Fillling()
    return render(request, 'profilefilling.html', {'form':form})

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
                # return redirect('main:login_account')
                return redirect('main:profile_filling') # redirect to profile filling or profile_filling_page
                
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