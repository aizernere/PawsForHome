function showPetModal(id, name, created, ageyears, agemonths, type, fee, description, imageUrl, isLiked) {
    document.getElementById('modalPetId').value = id;  
    document.getElementById('modalPetName').innerText = name;
    document.getElementById('modalPetCreated').innerText = "Uploaded on: " + created;
    document.getElementById('modalPetAgeYears').innerText = ageyears + " years";
    document.getElementById('modalPetAgeMonths').innerText = agemonths + " months";
    document.getElementById('modalPetType').innerText = type;
    document.getElementById('modalPetFee').innerText = fee;
    document.getElementById('modalPetDescription').innerText = description;
    document.getElementById('modalPetImage').src = imageUrl;

    // Set favorite icon based on whether it's liked
    // const favoriteIcon = isLiked ? '{% static "images/liked.png" %}' : '{% static "images/unliked.png" %}';
    const favoriteIcon = isLiked ? '/static/images/liked.png' : '/static/images/unliked.png';
    document.getElementById('modalFavoriteIcon').src = favoriteIcon;

    document.getElementById('petModal').classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
}

function toggleFavorite() {
    const petId = document.getElementById('modalPetId').value;  
    const currentIcon = document.getElementById('modalFavoriteIcon').src.includes('liked.png') 
        ? '{% static "images/unliked.png" %}' 
        : '{% static "images/liked.png" %}';

    document.getElementById('modalFavoriteIcon').src = currentIcon;
    // Optionally make an AJAX call or redirect to toggle the favorite status
    window.location.href = `/pets/toggle_favorite/${petId}/`;
}


function closePetModal() {
    document.getElementById('petModal').classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
}


function redirectToAdoptionForm() {
    const petId = document.getElementById('modalPetId').value;  
    window.location.href = `/adoptionform/${petId}/`; 
}