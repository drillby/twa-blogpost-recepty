let currentIndex = 0;

function changeMainImage(index) {
	currentIndex = index;
	document.getElementById("mainImage").src = images[index];
}

function openOverlay(index) {
	currentIndex = index;
	document.getElementById("overlayImage").src = images[index];
	document.getElementById("overlay").style.visibility = "visible";
}

function nextImage() {
	currentIndex = (currentIndex + 1) % images.length;
	document.getElementById("overlayImage").src = images[currentIndex];
}

function prevImage() {
	currentIndex = (currentIndex - 1 + images.length) % images.length;
	document.getElementById("overlayImage").src = images[currentIndex];
}

document.getElementById("overlay").addEventListener("click", function (event) {
	if (event.target === this) {
		this.style.visibility = "hidden";
	}
});

document.addEventListener("keydown", function (event) {
	if (event.key === "Escape") {
		document.getElementById("overlay").style.visibility = "hidden";
	}
});

function toggleFavorite() {
	console.log("Favorite button clicked");
	const button = document.querySelector(".favorite-button");
	const icon = button.querySelector("i");
	button.classList.toggle("active");
	if (button.classList.contains("active")) {
		icon.classList.remove("bi-heart");
		icon.classList.add("bi-heart-fill");
		button.innerHTML = '<i class="bi bi-heart-fill"></i> Odebrat z oblíbených';
	} else {
		icon.classList.remove("bi-heart-fill");
		icon.classList.add("bi-heart");
		button.innerHTML = '<i class="bi bi-heart"></i> Přidat do oblíbených';
	}
	// Add logic to handle adding/removing from favorites
}
