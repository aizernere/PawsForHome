from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pet, AdoptionRequest, Favorite
from .forms import PetForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages
from django.db import transaction

@login_required 
def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False) 
            pet.owner = request.user
            pet.location = request.user.address
            pet.save() 
            return redirect('main:pet_listings')
    else:
        form = PetForm()
    return render(request, 'pets/add_pet.html', {'form': form})

@login_required
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if pet.owner != request.user:
        messages.error(request, "You do not have permission to delete this pet.")
        return redirect('main:shelterdashboard')
    
    if request.method == "POST":
        with transaction.atomic():
            # Delete related adoption requests and favorites
            AdoptionRequest.objects.filter(pet=pet).delete()
            Favorite.objects.filter(pet=pet).delete()
            
            # Delete the pet
            pet.delete()
        
        messages.success(request, "Pet and all related data deleted successfully.")
        return redirect('main:shelterdashboard')
    
    return render(request, 'pets/confirm_delete.html', {'pet': pet})

@login_required
def edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('main:pet_listings')  # Redirect to the pet listings page
    else:
        form = PetForm(instance=pet)

    return render(request, 'pets/edit_pet.html', {'form': form, 'pet': pet})


@login_required
def list_pet(request):
    # Get IDs of pets for which the current user has pending adoption requests
    pending_requests_pet_ids = AdoptionRequest.objects.filter(account=request.user, status=1).values_list('pet_id', flat=True)

    # Retrieve the list of selected pet types, age, and location from the GET request
    selected_pet_types = request.GET.getlist('pet_type')  # Use getlist to get multiple values
    age_years = request.GET.get('age_years')
    age_months = request.GET.get('age_months')
    location = request.GET.get('location')

    # Start the queryset with the basic filter (status and excluding pets with pending adoption requests)
    pets_list = Pet.objects.filter(status=1).exclude(id__in=pending_requests_pet_ids)

    # Filter by pet types if provided
    if selected_pet_types:
        pets_list = pets_list.filter(type__in=selected_pet_types)

    # Filter by age if provided
    if age_years:
        pets_list = pets_list.filter(age_years__gte=age_years)  # Filter pets older than the specified years
    if age_months:
        pets_list = pets_list.filter(age_months__gte=age_months)  # Filter pets older than the specified months

    # Filter by location if provided
    if location:
        pets_list = pets_list.filter(location__icontains=location)  # Perform case-insensitive search

    # Pagination setup
    paginator = Paginator(pets_list, 10)
    page_number = request.GET.get('page')
    pets = paginator.get_page(page_number)

    # Get favorite pet IDs for the current user
    favorite_pet_ids = Favorite.objects.filter(user=request.user).values_list('pet_id', flat=True)

    # Pet type choices to pass to the template
    pet_type_choices = Pet.TYPE_CHOICES

    # Return rendered page with pets, favorite pet IDs, and pet type filter information
    return render(request, 'pets/list_pet.html', {
        'pets': pets,
        'favorite_pet_ids': favorite_pet_ids,
        'selected_pet_types': selected_pet_types,
        'pet_type_choices': pet_type_choices,
        'age_years': age_years,
        'age_months': age_months,
        'location': location,
    })

@login_required
def my_pets(request):
    pets = Pet.objects.filter(owner=request.user) 
    return render(request, 'shelterdashboard/pet_listings.html', {'pets': pets})

@login_required
def petsadopted(request):
    pets = Pet.objects.filter(owner=request.user, status=2) #dapat mu check sa adoption history since ang owner is ang new adopter
    return render(request, 'shelterdashboard/petsadopted.html', {'pets': pets})

@login_required
def dashpets(request):
    pets = Pet.objects.filter(owner=request.user, status=1) 
    pet_count = pets.count()
    #to do pending request
    adoption_requests = AdoptionRequest.objects.filter(pet__in=pets,status = 1)
    pending_count = adoption_requests.count()

    popular_pets = (
        pets.annotate(favorites_count=Count('favorite'))
        .filter(favorites_count__gt=0)
        .order_by('-favorites_count')
    )


    adopted_count = Pet.objects.filter(owner=request.user, status=2).count()
    return render(request, 'shelterdashboard.html', {
        'pets': pets,
        'pet_count': pet_count,
        'pending_count': pending_count,
        'adopted_count': adopted_count,
        'popular_pets': popular_pets,
    })
# @login_required
# def dashpets(request):
#     pets = Pet.objects.filter(owner=request.user) 
#     pet_count = pets.count()

#     shelter = request.user 
#     pets_request = Pet.objects.filter(owner=shelter)
#     adoption_requests = AdoptionRequest.objects.filter(pet__in=pets_request, status=1)
    
#     pending_count = adoption_requests.count()
#     adopted_count = pets.filter(status=2).count()

#     return render(request, 'shelterdashboard.html', {
#         'pets': pets,
#         'pet_count': pet_count,
#         'pending_count': pending_count,
#         'adopted_count': adopted_count,
#         'adoption_requests': adoption_requests,  
#     })

@login_required
def accept_adoption_request(request, request_id):
    adoption_request = get_object_or_404(AdoptionRequest, id=request_id)
    adoption_request.accept()
    return redirect('main:shelterdashboard')

@login_required
def reject_adoption_request(request, request_id):
    # print("Reject button clicked for adoption request ID:", request_id)
    adoption_request = get_object_or_404(AdoptionRequest, id=request_id)
    adoption_request.reject()
    return redirect('main:shelterdashboard')

@login_required
def toggle_favorite(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    
    # Get or create the favorite record
    favorite = Favorite.objects.filter(user=request.user, pet=pet).first()

    if favorite:
        # If the pet is already a favorite, remove it
        favorite.delete()
        status = 'unliked'
    else:
        # If the pet is not a favorite, add it
        Favorite.objects.create(user=request.user, pet=pet)
        status = 'liked'

    # Return a JSON response with the updated status
    return JsonResponse({'status': status})
    