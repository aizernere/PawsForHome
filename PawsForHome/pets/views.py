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
            # Mark related adoption requests as canceled or handled
            AdoptionRequest.objects.filter(pet=pet).update(status=3)  # Mark as rejected
            Favorite.objects.filter(pet=pet).delete()  # Remove favorites
            
            # Mark the pet as deleted
            pet.is_deleted = True
            pet.save()

        messages.success(request, f"{pet.name} has been marked as deleted.")
        return redirect('main:shelterdashboard')

    return render(request, 'pets/confirm_delete.html', {'pet': pet})

@login_required
def restore_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, is_deleted=True)

    if request.method == "POST":
        # Mark the pet as not deleted
        pet.is_deleted = False
        pet.save()
        messages.success(request, f"{pet.name} has been restored successfully.")
        return redirect('main:shelterdashboard')

    return render(request, 'pets/confirm_restore.html', {'pet': pet})



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

    # Get the list of pets that are available for adoption and do not have pending requests
    pets_list = Pet.objects.filter(status=1,is_deleted=False).exclude(id__in=pending_requests_pet_ids)

    paginator = Paginator(pets_list, 10)
    page_number = request.GET.get('page')
    pets = paginator.get_page(page_number)

    favorite_pet_ids = Favorite.objects.filter(user=request.user).values_list('pet_id', flat=True)

    return render(request, 'pets/list_pet.html', {
        'pets': pets,
        'favorite_pet_ids': favorite_pet_ids,
    })

@login_required
def my_pets(request):
    pets = Pet.objects.filter(owner=request.user,is_deleted=False) 
    deleted_pets = Pet.objects.filter(owner=request.user,is_deleted=True)
    context = {
        'pets': pets,
        'deleted_pets': deleted_pets,
    }
    return render(request, 'shelterdashboard/pet_listings.html', context)

@login_required
def petsadopted(request):
    pets = Pet.objects.filter(owner=request.user, status=2) #dapat mu check sa adoption history since ang owner is ang new adopter
    return render(request, 'shelterdashboard/petsadopted.html', {'pets': pets})

@login_required
def dashpets(request):
    pets = Pet.objects.filter(owner=request.user, status=1,is_deleted=False) 
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
    