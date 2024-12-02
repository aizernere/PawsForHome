function showPetModal(id, name, created, ageyears, agemonths, type, fee, description, imageUrl, isRequested=null) {
    document.getElementById('modalPetId').value = id;  
    document.getElementById('modalPetName').innerText = name;
    document.getElementById('modalPetCreated').innerText = "Uploaded on: " + created;
    document.getElementById('modalPetAgeYears').innerText = ageyears + " years";
    document.getElementById('modalPetAgeMonths').innerText = agemonths + " months";
    document.getElementById('modalPetType').innerText = type;
    document.getElementById('modalPetFee').innerText = fee;
    document.getElementById('modalPetDescription').innerText = description;
    document.getElementById('modalPetImage').src = imageUrl;

    const favoriteIcon = document.getElementById('modalFavoriteIcon');

    if (isRequested !== null) {
        const btn = document.getElementById('modalApplyButton');
        if (isRequested) btn.classList.add('hidden');
        else btn.classList.remove('hidden');
    }

    // Get the favorite status from the browse section
    const petCard = document.querySelector(`[data-pet-id="${id}"]`);
    const browseFavoriteIcon = petCard.querySelector('.favorite-icon');
    const isLiked = browseFavoriteIcon.dataset.favorited === 'true';

    // Update the modal's favorite icon state
    favoriteIcon.src = isLiked ? '/static/images/liked.png' : '/static/images/unliked.png';
    favoriteIcon.dataset.favorited = isLiked ? 'true' : 'false';

    // Remove any existing click listeners to avoid duplicate handlers
    favoriteIcon.replaceWith(favoriteIcon.cloneNode(true));
    const newFavoriteIcon = document.getElementById('modalFavoriteIcon');
    newFavoriteIcon.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevent the modal's close action
        toggleFavorite(event, id, newFavoriteIcon); // Pass the event explicitly to the function
    });

    document.getElementById('petModal').classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
}

function toggleFavorite(event, petId, favoriteIcon) {
    event.stopPropagation(); // Prevent the parent div's onclick from triggering

    var favoriteIcon = event.target;

    // If the image is wrapped in an <a> tag, get the <img> inside
    if (favoriteIcon.tagName !== 'IMG') {
        favoriteIcon = favoriteIcon.querySelector('img');
    }

    var isFavorited = favoriteIcon.dataset.favorited === 'true';

    var newStatus = isFavorited ? 'unlike' : 'like';

    // Get CSRF token from the meta tag
    var csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    fetch(`/pets/toggle_favorite/${petId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: newStatus, pet_id: petId }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'liked') {
            favoriteIcon.src = '/static/images/liked.png';
            favoriteIcon.dataset.favorited = 'true';
            updateBrowseFavoriteIcon(petId, true);
        } else {
            favoriteIcon.src = '/static/images/unliked.png';
            favoriteIcon.dataset.favorited = 'false';
            updateBrowseFavoriteIcon(petId, false);
        }
    })
    .catch(error => console.error('Error:', error));

}

function updateBrowseFavoriteIcon(petId, isFavorited) {
    const petCard = document.querySelector(`[data-pet-id="${petId}"]`);
    if (petCard) {
        const favoriteIcon = petCard.querySelector('.toggle-favorite img'); 
        if (favoriteIcon) {
            favoriteIcon.src = isFavorited ? '/static/images/liked.png' : '/static/images/unliked.png';
        }
    }
}


function closePetModal() {
    document.getElementById('petModal').classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
}


function redirectToAdoptionForm() {
    const petId = document.getElementById('modalPetId').value;  
    window.location.href = `/adoptionform/${petId}/`; 
}