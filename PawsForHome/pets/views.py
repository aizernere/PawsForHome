from django.shortcuts import render, redirect
from .models import Pet
from .forms import PetForm

def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_pet')
    else:
        form = PetForm()
    return render(request, 'pets/add_pet.html', {'form': form})

def list_pet(request):
    pets = Pet.objects.all()
    return render(request, 'pets/list_pet.html', {'pets': pets})