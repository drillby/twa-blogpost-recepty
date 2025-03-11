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

document.addEventListener("DOMContentLoaded", function () {
	console.log("🔹 JavaScript načten správně!");

	const favoriteButton = document.querySelector(".favorite-button");

	if (favoriteButton) {
		favoriteButton.addEventListener("click", function () {
			const recipeId = this.getAttribute("data-recipe-id");
			console.log("🔹 Klik na tlačítko! ID receptu:", recipeId);

			fetch(`/toggle-favorite/${recipeId}`, {
				method: "POST",
				headers: {
					"X-Requested-With": "XMLHttpRequest",
				},
			})
				.then((response) => response.json())
				.then((data) => {
					console.log("🔹 Odpověď serveru:", data);

					if (data.status === "error") {
						alert(data.message);
						return;
					}

					const icon = favoriteButton.querySelector("i");

					if (data.status === "added") {
						icon.classList.remove("bi-heart");
						icon.classList.add("bi-heart-fill");
						favoriteButton.innerHTML =
							'<i class="bi bi-heart-fill"></i> Odebrat z oblíbených';
					} else if (data.status === "removed") {
						icon.classList.remove("bi-heart-fill");
						icon.classList.add("bi-heart");
						favoriteButton.innerHTML =
							'<i class="bi bi-heart"></i> Přidat do oblíbených';
					}
				})
				.catch((error) => console.error("❌ Chyba v AJAX požadavku:", error));
		});
	} else {
		console.log("❌ CHYBA: Tlačítko nebylo nalezeno!");
	}
});
