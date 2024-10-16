from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import Account
from .forms import Create_Account, Login_Account, Profile_Filling
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import AdoptionForm
from pets.models import Pet, AdoptionRequest

# Create your views here.

def landing_page(request):
    if request.user.is_authenticated:
        return index(request)
    return render(request, 'landing_page.html', {})
def index(request):
    return render(request, 'index.html', {})
def features(request):
    return render(request, 'features.html', {})
def contactus(request):
    return render(request, 'contactus.html', {})
# def adoptionform(request):
#     return render(request, 'adoptionform.html', {})
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

@login_required
def profile_filling(request):
    
    curr_account = request.user

    if request.method == 'POST':
        form = Profile_Filling(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            birthdate = form.cleaned_data.get('birthdate')
            phone_num = form.cleaned_data.get('phone_number')
            address = form.cleaned_data.get('address')

            if phone_num and first_name and last_name and birthdate:
                phone_len = len(str(phone_num))
                if phone_len != 11:
                    messages.warning(request, 'Input 11 digit number')
                else: 
                    curr_account.first_name = first_name
                    curr_account.last_name = last_name
                    curr_account.birth_date = birthdate
                    curr_account.phone_number = phone_num
                    curr_account.address = address

                    curr_account.save()

                    return redirect('main:profile')
        else:
            messages.warning(request, 'All fields are required')

    else:
        form = Profile_Filling()
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
                return redirect('main:login_account')
                #return redirect('main:profile_filling') 
                
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

@login_required
def adoption_request_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    
    # Fetch the user's profile data
    user_profile = request.user  # Assuming `Account` model is linked to the logged-in user

    if request.method == 'POST':
        form = AdoptionForm(request.POST)
        if form.is_valid():
            adoption_request = form.save(commit=False)
            adoption_request.pet = pet
            adoption_request.account = user_profile  # Link the adoption request to the user's profile
            adoption_request.save()
            return redirect('pets:list_pet')  # Redirect to a success page
    else:
        # Prepopulate the form with the user's profile data
        form = AdoptionForm(initial={
            'first_name': user_profile.first_name,
            'last_name': user_profile.last_name,
            'email': user_profile.email,
            'phone_number': user_profile.phone_number,
            'address': user_profile.address,
        })

    return render(request, 'adoptionform.html', {
        'form': form,
        'pet': pet,
    })