from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import Account
from .forms import Create_Account, Login_Account, Profile_Filling, ProfileEdit
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import AdoptionForm
from pets.models import Pet, AdoptionRequest, Favorite

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

def ud_requests(request):
    user_request = AdoptionRequest.objects.filter(account_id=request.user.id)
    # print(user_request)
    pet_ids = user_request.filter(status=1).values_list('pet_id', flat=True)
    request_pets = Pet.objects.filter(id__in=pet_ids)
    # print(request_pets)
    curr_fn = request.user.first_name

    favorite_pet_ids = Favorite.objects.filter(user=request.user).values_list('pet_id', flat=True)

    return render(request, 'user_dashboard/requests.html', {
        'request_pets':request_pets, 
        'curr_fn':curr_fn,
        'favorite_pet_ids':favorite_pet_ids
        })

def ud_favorites(request):
    curr_fn = request.user.first_name
    user_favorites = Favorite.objects.filter(user_id = request.user.id).values_list('pet_id', flat=True)
    fav_pets = Pet.objects.filter(id__in=user_favorites)

    pet_requested = AdoptionRequest.objects.filter(account_id = request.user.id).values_list('pet_id', flat=True)
    return render(request, 'user_dashboard/favorites.html', {
        'curr_fn': curr_fn, 
        'fav_pets':fav_pets,
        'pet_requested':pet_requested
        })

def ud_adoptionhistory(request):
    curr_fn = request.user.first_name

    # user_requests = AdoptionRequest.objects.filter(account_id = request.user.id)
    user_requests = AdoptionRequest.objects.filter(
        account_id = request.user.id,
        status__in=[2, 3]
        )
    
    status_map = {req.pet_id: req.status for req in user_requests}

    request_pets = Pet.objects.filter(id__in=status_map.keys())
    # request_pets = Pet.objects.filter(id__in=user_requests.values_list('pet_id', flat=True))

    # accepted = Pet.objects.filter(id__in = user_requests.filter(status = 2).values_list('pet_id', flat=True))
    # rejected = Pet.objects.filter(id__in = user_requests.filter(status = 3).values_list('pet_id', flat=True))
    
    # return render(request, 'user_dashboard/adoption_history.html', {
    #     'curr_fn':curr_fn,
    #     'accepted':accepted,
    #     'rejected':rejected
    #     })
    # pets_with_status = [
    #     {
    #         'request_pet': request_pet,
    #         'status': status_map.get(request_pet.id, None),
    #     }
    #     for request_pet in request_pets
    # ]
    pets_with_status = [
        {
            'request_pet': request_pet,
            'status': status_map[request_pet.id],
        }
        for request_pet in request_pets
    ]
    return render(request, 'user_dashboard/adoption_history.html', {
        'curr_fn':curr_fn,
        'pets_with_status':pets_with_status
        # 'user_requests':user_requests,
        # 'request_pets':request_pets,
        # 'status_map':status_map
        })
    
# def adoptionform(request):
#     return render(request, 'adoptionform.html', {})
def shelterdashboard(request):
    return render(request, 'shelterdashboard.html', {})

@login_required
def user_dashboard(request):
    curr_fn = request.user.first_name

    user_requests = AdoptionRequest.objects.filter(account_id = request.user.id)
    
    # pets owned count and not count
    pets = user_requests.filter(status=2).values_list('pet_id', flat=True)
    own_pet = Pet.objects.filter(id__in = pets)
    own_pet_count = user_requests.filter(status = 2).count()

    # request count
    request_count = user_requests.filter(status=1).count()

    # favorite pets count
    fave_count = Favorite.objects.filter(user_id = request.user.id).count()

    return render(request, 'userdashboard.html', {
        'curr_fn':curr_fn,
        'own_pet':own_pet,
        'own_pet_count':own_pet_count,
        'request_count':request_count,
        'fave_count':fave_count
        })

def petsadopted(request):
    return render(request, 'shelterdashboard/petsadopted.html',{})
def pet_listings(request):
    return render(request, 'shelterdashboard/pet_listings.html',{})
def adoptform(request):
    return render(request, 'shelterdashboard/adoptform.html',{})
# def pending_requests(request):
#     return render(request, 'shelterdashboard/pending_requests.html',{})
# def notifications(request):
#     return render(request, 'navbar/notifications.html', {})

@login_required
def notifications(request):
    notifications = request.user.notifications.all().order_by("-created_at")
    return render(request, "navbar/notifications.html", {"notifications": notifications})
# def message(request):
#     return render(request, 'navbar/message.html', {})

@login_required
def profile(request):
    user_profile = request.user

    if request.method == 'POST':
        form = ProfileEdit(request.POST)
        if form.is_valid():
            user_profile.first_name = form.cleaned_data['first_name']
            user_profile.last_name = form.cleaned_data['last_name']
            user_profile.birth_date = form.cleaned_data['birthdate']
            user_profile.phone_number = form.cleaned_data['phone_number']
            user_profile.address = form.cleaned_data['address']
            user_profile.email = form.cleaned_data['email']
            new_password = form.cleaned_data.get('password')
            
            if new_password:
                user_profile.set_password(new_password)
            
            user_profile.save()
            login(request, user_profile)
            return redirect('main:profile')
    else:
        form = ProfileEdit(initial={
            'first_name': user_profile.first_name,
            'last_name': user_profile.last_name,
            'birthdate': user_profile.birth_date,
            'phone_number': user_profile.phone_number,
            'address': user_profile.address,
            'email': user_profile.email,
        })

    return render(request, 'navbar/profile.html', {
        'curr_fn':user_profile.first_name,
        'form': form
    })

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

                    # return redirect('main:profile')
                    return redirect('main:home')
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
                first_login = user.last_login is None
                login(request, user)
                if first_login:
                    return redirect('main:profile_filling')
                else:
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
    user_profile = request.user

    if request.method == 'POST':
        form = AdoptionForm(request.POST)
        if form.is_valid():
            adoption_request = form.save(commit=False)
            adoption_request.pet = pet
            adoption_request.account = user_profile
            adoption_request.status = 1 
            adoption_request.save()
            
            return redirect('pets:list_pet')
    else:
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


# @login_required
# def pending_requests(request):
#     shelter = request.user 
#     pets = Pet.objects.filter(owner=shelter,status=3)
#     adoption_requests = AdoptionRequest.objects.filter(pet__in=pets)
    
#     context = {
#         'adoption_requests': adoption_requests,
#         'pets': pets,
#     }
#     return render(request, 'shelterdashboard/pending_requests.html', context)
@login_required
def pending_requests(request):
    shelter = request.user
    pets = Pet.objects.filter(owner=shelter)
    adoption_requests = AdoptionRequest.objects.filter(pet__in=pets, status=1)  

    context = {
        'adoption_requests': adoption_requests,
        'pets': pets,
    }
    return render(request, 'shelterdashboard/pending_requests.html', context)


@login_required
def adoption_request_detail(request, request_id):
    adoption_request = get_object_or_404(AdoptionRequest, id=request_id)
    return render(request, 'shelterdashboard/adoptform.html', {'adoption_request': adoption_request, 'request': request})