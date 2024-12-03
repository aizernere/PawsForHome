window.onload = function () {
    slideOne();
    slideTwo();
    bindSpanListeners();
};

let sliderOne = document.getElementById("slider-1");
let sliderTwo = document.getElementById("slider-2");
let displayValOne = document.getElementById("range1");
let displayValTwo = document.getElementById("range2");
let errorMessageOne = document.getElementById("error-message-one");
let errorMessageTwo = document.getElementById("error-message-two");
let minGap = 0;
let sliderTrack = document.querySelector(".slider-track");
let sliderMaxValue = 100; // Set max value to 100

function slideOne() {
    if (parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap) {
        sliderOne.value = parseInt(sliderTwo.value) - minGap;
    }
    displayValOne.textContent = sliderOne.value;
    errorMessageOne.classList.add("hidden");
    fillColor();
}

function slideTwo() {
    if (parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap) {
        sliderTwo.value = parseInt(sliderOne.value) + minGap;
    }
    displayValTwo.textContent = sliderTwo.value;
    errorMessageTwo.classList.add("hidden");
    fillColor();
}

function fillColor() {
    let percent1 = (sliderOne.value / sliderMaxValue) * 100;
    let percent2 = (sliderTwo.value / sliderMaxValue) * 100;
    sliderTrack.style.background = `linear-gradient(to right, #dadae5 ${percent1}%, #f97316 ${percent1}%, #f97316 ${percent2}%, #dadae5 ${percent2}%)`;
}

function bindSpanListeners() {
    displayValOne.addEventListener("input", function () {
        validateAndUpdate(this, sliderOne, errorMessageOne, slideOne);
    });

    displayValTwo.addEventListener("input", function () {
        validateAndUpdate(this, sliderTwo, errorMessageTwo, slideTwo);
    });
}

function validateAndUpdate(span, slider, errorMessage, slideFn) {
    const value = span.textContent.trim();

    if (value === "" || isNaN(value)) {
        errorMessage.classList.remove("hidden");
        return;
    }

    const numericValue = Math.max(0, Math.min(parseInt(value), sliderMaxValue));
    slider.value = numericValue;
    slideFn();
}
