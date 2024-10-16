from django.shortcuts import render, redirect
from .models import Pet
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
def dashpets(request):
    pets = Pet.objects.filter(owner=request.user) 
    pet_count = pets.count()
    #to do pending request

    return render(request, 'shelterdashboard.html', {'pets': pets, 'pet_count': pet_count})