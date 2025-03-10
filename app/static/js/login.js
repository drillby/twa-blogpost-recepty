function validateLoginForm() {
	let isValid = true;

	const username = document.getElementById("username").value;
	const password = document.getElementById("password").value;

	document.getElementById("usernameError").textContent = "";
	document.getElementById("passwordError").textContent = "";

	if (!username) {
		document.getElementById("usernameError").textContent =
			"Uživatelské jméno je povinné.";
		isValid = false;
	}
	if (!password) {
		document.getElementById("passwordError").textContent = "Heslo je povinné.";
		isValid = false;
	}

	return isValid;
}
