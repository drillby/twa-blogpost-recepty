setTimeout(function () {
	var alerts = document.querySelectorAll(".alert");
	alerts.forEach(function (alert) {
		var bsAlert = new bootstrap.Alert(alert);
		bsAlert.close();
	});
}, 5000);

document.getElementById("load-more").addEventListener("click", function () {
	let button = this;
	let page = parseInt(button.getAttribute("data-page")) + 1;

	fetch(`/?page=${page}`)
		.then((response) => response.text())
		.then((data) => {
			let parser = new DOMParser();
			let doc = parser.parseFromString(data, "text/html");

			let recipeList = document.getElementById("recipe-list");
			let newRecipes = doc.querySelectorAll(".recipe-card");
			newRecipes.forEach((recipe) => {
				recipeList.appendChild(recipe);
			});

			button.setAttribute("data-page", page);

			if (!doc.querySelector("#load-more").hasAttribute("data-page")) {
				button.hidden = true;
			}
		})
		.catch((error) => console.error("Chyba při načítání receptů:", error));
});

try {
	const now = new Date();
	let clientHour = now.getHours();

	if (isNaN(clientHour)) {
		throw new Error("Chybný čas");
	}

	fetch(`/?time=${clientHour}`, { method: "GET" })
		.then((response) => response.text())
		.then((data) => console.log(data))
		.catch((error) =>
			console.error("Chyba při odesílání času na server:", error)
		);
} catch (error) {
	console.warn(
		"Nepodařilo se získat aktuální hodinu, používá se serverový čas."
	);
	fetch(`/?time=NaN`, { method: "GET" });
}
