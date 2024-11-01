from django.shortcuts import render, redirect, get_object_or_404
from .models import Pet, AdoptionRequest, Favorite
from .forms import PetForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Count

@login_required 
def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False) 
            pet.owner = request.user
            pet.save() 
            return redirect('main:pet_listings')
    else:
        form = PetForm()
    return render(request, 'pets/add_pet.html', {'form': form})


def list_pet(request):
    pets_list = Pet.objects.filter(status__in=[1, 2])
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
    pets = Pet.objects.filter(owner=request.user) 
    return render(request, 'shelterdashboard/pet_listings.html', {'pets': pets})

@login_required
def petsadopted(request):
    pets = Pet.objects.filter(owner=request.user, status=3) #dapat mu check sa adoption history since ang owner is ang new adopter
    return render(request, 'shelterdashboard/petsadopted.html', {'pets': pets})

@login_required
def dashpets(request):
    pets = Pet.objects.filter(owner=request.user, status__in=[1, 2]) 
    pet_count = pets.count()
    #to do pending request
    shelter = request.user 
    pets = Pet.objects.filter(owner=shelter, status=1)
    adoption_requests = AdoptionRequest.objects.filter(pet__in=pets,status =1)
    pending_count = adoption_requests.count()

    popular_pets = (
        pets.annotate(favorites_count=Count('favorite'))
        .filter(favorites_count__gt=0)
        .order_by('-favorites_count')
    )


    adopted_count = Pet.objects.filter(owner=request.user, status=3).count()
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
    favorite, created = Favorite.objects.get_or_create(user=request.user, pet=pet)
    if not created:
        favorite.delete()
    return redirect('pets:list_pet')