from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import Account, Notification
from .forms import Create_Account, Login_Account, Profile_Filling, ProfileEdit
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import AdoptionForm
from pets.models import Pet, AdoptionRequest, Favorite
from .decorators import adopter_required, shelter_required
from pmessages.models import Message
from django.utils import timezone
import re

# Create your views here.

def error404(request):
    return render(request, '404.html', {})

def landing_page(request):
    if request.user.is_authenticated:
        return home(request)
    return render(request, 'landing_page.html', {})
def index(request):
    return render(request, 'index.html', {})
def features(request):
    return render(request, 'features.html', {})
def contactus(request):
    return render(request, 'contactus.html', {})

@login_required
@adopter_required
def ud_requests(request):
    if not request.user.is_authenticated:
        return render(request, 'error404.html', {})

    user_request = AdoptionRequest.objects.filter(account_id=request.user.id)
    # print(user_request)
    pet_ids = user_request.filter(status=1).values_list('pet_id', flat=True)
    request_pets = Pet.objects.filter(id__in=pet_ids)
    # print(request_pets)
    curr_fn = request.user.first_name

    curr_account = request.user

    favorite_pet_ids = Favorite.objects.filter(user=request.user).values_list('pet_id', flat=True)

    return render(request, 'user_dashboard/requests.html', {
        'request_pets':request_pets, 
        'curr_fn':curr_fn,
        'favorite_pet_ids':favorite_pet_ids,
        'curr': curr_account
        })

@login_required
@adopter_required
def ud_favorites(request):
    if not request.user.is_authenticated:
        return render(request, 'error404.html', {})

    curr_fn = request.user.first_name
    user_favorites = Favorite.objects.filter(user_id = request.user.id).values_list('pet_id', flat=True)
    fav_pets = Pet.objects.filter(id__in=user_favorites)

    curr_account = request.user
    pet_requested = AdoptionRequest.objects.filter(account_id = request.user.id).values_list('pet_id', flat=True)
    return render(request, 'user_dashboard/favorites.html', {
        'curr_fn': curr_fn, 
        'fav_pets':fav_pets,
        'pet_requested':pet_requested,
        'curr': curr_account
        })

@login_required
@adopter_required
def ud_adoptionhistory(request):
    if not request.user.is_authenticated:
        return render(request, 'error404.html', {})

    curr_fn = request.user.first_name
    curr_account = request.user

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
        'pets_with_status':pets_with_status,
        'curr': curr_account,
        # 'user_requests':user_requests,
        # 'request_pets':request_pets,
        # 'status_map':status_map
        })
    
# def adoptionform(request):
#     return render(request, 'adoptionform.html', {})
@login_required
def shelterdashboard(request):
    print(request.user.first_name)  #
    # print(f"User's account type: {request.user.account_type}") 
    
    # if request.user.account_type != 'shelter':
    #     print("Access denied")  
    #     return HttpResponseForbidden("You are not authorized.")
    
    return render(request, 'shelterdashboard.html', {})

@login_required
@adopter_required
def user_dashboard(request):
    if not request.user.is_authenticated:
        return render(request, 'error404.html', {})

    curr_fn = request.user.first_name
    curr_account = request.user

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
        # 'curr_fn':curr_fn,
        'curr_fn':curr_fn,
        'own_pet':own_pet,
        'own_pet_count':own_pet_count,
        'request_count':request_count,
        'fave_count':fave_count,
        'curr': curr_account
        })

# @login_required
# def petsadopted(request):
#     return render(request, 'shelterdashboard/petsadopted.html',{})

# @login_required
# def pet_listings(request):
#     return render(request, 'shelterdashboard/pet_listings.html',{})

# @login_required
# def adoptform(request):
#     return render(request, 'shelterdashboard/adoptform.html',{})
# def pending_requests(request):
#     return render(request, 'shelterdashboard/pending_requests.html',{})
# def notifications(request):
#     return render(request, 'navbar/notifications.html', {})

@login_required(login_url='/login/')
def notifications(request):
    if not request.user.is_authenticated:
        return render(request, 'error404.html', {})

    notifications = request.user.notifications.all().order_by("-created_at")
    return render(request, "navbar/notifications.html", {"notifications": notifications})
# def message(request):
#     return render(request, 'navbar/message.html', {})

@login_required(login_url='/login/')
def profile(request):
    if not request.user.is_authenticated:
        return render(request, 'error404.html', {})

    user_profile = request.user
    pattern = r"^[A-Za-z\s\-']+$"

    if request.method == 'POST':
        form = ProfileEdit(request.POST, request.FILES)

        if form.is_valid():
            new_firstname = form.cleaned_data['first_name']
            new_lastname = form.cleaned_data['last_name']
            new_birthdate = form.cleaned_data['birthdate']
            new_phone_num = form.cleaned_data['phone_number']
            new_address = form.cleaned_data['address']
            new_email = form.cleaned_data['email']
            new_password = form.cleaned_data.get('password')
            new_profile_pic = request.FILES.get('update-image')
            
            if new_phone_num and new_firstname and new_lastname and new_birthdate and new_email:
                phone_len = len(str(new_phone_num))
                if phone_len != 11:
                    form.add_error('phone_number', "Phone number must be exactly 11 digits.")
                    # messages.warning(request, 'Input 11 digit number')
                #     # return redirect('main:profile')
                # else:
                #     user_profile.phone_number = new_phone_num
                # elif not new_firstname.replace(" ", "").isalpha():
                #     messages.warning(request, 'First name should only contain letters.')
                # elif not new_lastname.replace(" ", "").isalpha():
                #     messages.warning(request, 'Last name should only contain letters.')
                # elif not re.match(pattern, new_firstname):
                #     messages.warning(request, 'First name should only contain letters.')
                #     return redirect('main:profile')
                # elif not re.match(pattern, new_lastname):
                #     messages.warning(request, 'Last name should only contain letters.')
                #     return redirect('main:profile')
                
                if not re.match(pattern, new_firstname):
                    form.add_error('first_name', 'First name should only contain letters.')
                    # messages.warning(request, 'First name should only contain letters.')
                    # return redirect('main:profile')
                else:
                    user_profile.first_name = new_firstname

                if not re.match(pattern, new_lastname):
                    form.add_error('last_name', 'Last name should only contain letters.')
                    # messages.warning(request, 'Last name should only contain letters.')
                    # return redirect('main:profile')
                else:
                    user_profile.last_name = new_lastname
                
                if form.errors:
                    return render(request, 'navbar/profile.html', {
                        'curr_fn':user_profile.first_name,
                        'curr_ln':user_profile.last_name,
                        'form': form,
                        'user': user_profile,
                        'type': user_profile.account_type
                    })

                # if phone_len != 11 or not re.match(pattern, new_firstname) or not re.match(pattern, new_lastname):
                #     # messages.warning(request, 'Invalid input')
                #     return redirect('main:profile')
                
                if new_password:
                    user_profile.set_password(new_password)
                # if user_profile.first_name != new_firstname:
                #     user_profile.first_name = new_firstname
                # if user_profile.last_name != new_lastname:
                #     user_profile.last_name = new_lastname
                if user_profile.birth_date != new_birthdate:
                    user_profile.birth_date = new_birthdate
                # if user_profile.phone_number != new_phone_num:
                #     user_profile.phone_number = new_phone_num
                if user_profile.address != new_address:
                    user_profile.address = new_address  
                if user_profile.email != new_email:
                    user_profile.email = new_email
                # if user_profile.image != new_profile_pic:
                # user_profile.image = new_profile_pic
                user_profile.image = new_profile_pic
                

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
        'curr_ln':user_profile.last_name,
        'form': form,
        'user': user_profile,
        'type': user_profile.account_type
    })

@login_required
def home(request):
    return render(request, 'home.html', {})

@login_required
def profile_filling(request):
    if not request.user.is_authenticated:
        return render(request, 'error404.html', {})

    
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
            
            # Authenticate the user
            user = authenticate(request, email=email, password=password)
            
            if user:
                first_login = user.last_login is None 
                login(request, user)
                
                if first_login:
                    messages.success(request, "Welcome! Please complete your profile information.")
                    return redirect('main:profile_filling')
                
                return redirect('main:home')
            else:
                messages.error(request, "Invalid email or password. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
        
       
        return render(request, 'login_signup/login.html', {'form': form})

    
    form = Login_Account()
    return render(request, 'login_signup/login.html', {'form': form})

@login_required
def logout_account(request):
    logout(request)
    return redirect('main:landing_page')

@login_required
@adopter_required
def adoption_request_view(request, pet_id):
    if not request.user.is_authenticated:
        return render(request, 'error404.html', {})

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
            input = f"Your adoption request for {pet.name} has been sent!"
            output = f"You have a new adoption request for {pet.name}!"
            messageinput = f"I have sent you an adoption request for {pet.name}. Please consider my request."
            Notification.objects.create(account=user_profile, notification=input)
            Notification.objects.create(account=pet.owner, notification=output)
            Message.objects.create(
                sender=user_profile,
                receiver=pet.owner, 
                content=messageinput,
                timestamp=timezone.now()
            )
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
@shelter_required
def pending_requests(request):

    shelter = request.user
    all_pets = Pet.objects.filter(owner=shelter)
    shelter_pets = all_pets.filter(status=1)

    selected_pet_id = request.GET.get('pet_id')
    if selected_pet_id:
        selected_pet = shelter_pets.filter(id=selected_pet_id).first()  # Ensure the pet belongs to the shelter
        adoption_requests = AdoptionRequest.objects.filter(
            pet=selected_pet, status=1
        ).order_by('id') if selected_pet else []
    else:
        adoption_requests = AdoptionRequest.objects.filter(
            pet__in=shelter_pets, status=1
        ).order_by('id')

    context = {
        'shelter_pets': shelter_pets,
        'adoption_requests': adoption_requests,
        'selected_pet_id': selected_pet_id
    }
    return render(request, 'shelterdashboard/pending_requests.html', context)


@login_required
@shelter_required
def adoption_request_detail_all(request, request_id):

    adoption_request = get_object_or_404(AdoptionRequest, id=request_id)
    shelter = request.user
    pets = Pet.objects.filter(owner=shelter)

    scanRequest = AdoptionRequest.objects.filter(pet__in=pets, status=1) 
    next_request = scanRequest.filter(
        id__gt=adoption_request.id, 
        pet__owner=request.user
    ).order_by('id').first()
    
    previous_request = scanRequest.filter(
        id__lt=adoption_request.id, 
        pet__owner=request.user
    ).order_by('-id').first()
    
    return render(request, 'shelterdashboard/adoptform_all.html', {
        'adoption_request': adoption_request,
        'next_request': next_request,
        'previous_request': previous_request,
    })

@login_required
@shelter_required
def adoption_request_detail(request, request_id):
    adoption_request = get_object_or_404(AdoptionRequest, id=request_id)
    shelter = request.user
    pets = Pet.objects.filter(owner=shelter)

    pet_id = request.GET.get('pet_id')
    if pet_id:
        selected_pet = pets.filter(id=pet_id).first()  # Ensure the pet belongs to the shelter
        if not selected_pet:
            return HttpResponseForbidden("You are not authorized to view this pet's requests.")
    else:
        selected_pet = adoption_request.pet  # Default to the pet in the current request

    scanRequest = AdoptionRequest.objects.filter(pet=selected_pet, status=1)

    next_request = scanRequest.filter(id__gt=adoption_request.id).order_by('id').first()
    previous_request = scanRequest.filter(id__lt=adoption_request.id).order_by('-id').first()

    return render(request, 'shelterdashboard/adoptform.html', {
        'adoption_request': adoption_request,
        'next_request': next_request,
        'previous_request': previous_request,
        'selected_pet': selected_pet,  # Pass the selected pet for additional context if needed
    })