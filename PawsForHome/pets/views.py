from django.shortcuts import render, redirect, get_object_or_404
from .models import Pet, AdoptionRequest
from .forms import PetForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

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
    pets_list = Pet.objects.all()
    paginator = Paginator(pets_list, 10)

    page_number = request.GET.get('page') 
    pets = paginator.get_page(page_number)

    return render(request, 'pets/list_pet.html', {'pets': pets})

@login_required
def my_pets(request):
    pets = Pet.objects.filter(owner=request.user) 
    return render(request, 'shelterdashboard/pet_listings.html', {'pets': pets})

@login_required
def petsadopted(request):
    pets = Pet.objects.filter(owner=request.user, status=2)
    return render(request, 'shelterdashboard/petsadopted.html', {'pets': pets})

@login_required
def dashpets(request):
    pets = Pet.objects.filter(owner=request.user) 
    pet_count = pets.count()
    #to do pending request
    shelter = request.user 
    pets_request = Pet.objects.filter(owner=shelter)
    adoption_requests = AdoptionRequest.objects.filter(pet__in=pets_request)
    pending_count = adoption_requests.count()

    adopted_count = pets.filter(status=2).count()
    return render(request, 'shelterdashboard.html', {
        'pets': pets,
        'pet_count': pet_count,
        'pending_count': pending_count,
        'adopted_count': adopted_count,
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
    adoption_request = get_object_or_404(AdoptionRequest, id=request_id)
    adoption_request.reject()
    return redirect('main:shelterdashboard')