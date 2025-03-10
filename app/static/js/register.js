function validateForm() {
	let isValid = true;

	const username = document.getElementById("username").value;
	const email = document.getElementById("email").value;
	const password = document.getElementById("password").value;
	const confirmPassword = document.getElementById("confirm_password").value;

	document.getElementById("usernameError").textContent = "";
	document.getElementById("emailError").textContent = "";
	document.getElementById("passwordError").textContent = "";
	document.getElementById("confirmPasswordError").textContent = "";

	if (!username) {
		document.getElementById("usernameError").textContent =
			"Uživatelské jméno je povinné.";
		isValid = false;
	}
	if (!email) {
		document.getElementById("emailError").textContent = "Email je povinný.";
		isValid = false;
	}
	if (!password) {
		document.getElementById("passwordError").textContent = "Heslo je povinné.";
		isValid = false;
	} else if (password.length < 8) {
		document.getElementById("passwordError").textContent =
			"Heslo musí mít alespoň 8 znaků.";
		isValid = false;
	} else if (!/[A-Z]/.test(password)) {
		document.getElementById("passwordError").textContent =
			"Heslo musí obsahovat alespoň jedno velké písmeno.";
		isValid = false;
	} else if (!/[a-z]/.test(password)) {
		document.getElementById("passwordError").textContent =
			"Heslo musí obsahovat alespoň jedno malé písmeno.";
		isValid = false;
	} else if (!/[0-9]/.test(password)) {
		document.getElementById("passwordError").textContent =
			"Heslo musí obsahovat alespoň jednu číslici.";
		isValid = false;
	} else if (!/[!@#$%^&*]/.test(password)) {
		document.getElementById("passwordError").textContent =
			"Heslo musí obsahovat alespoň jeden speciální znak (!@#$%^&*).";
		isValid = false;
	}
	if (password !== confirmPassword) {
		document.getElementById("confirmPasswordError").textContent =
			"Hesla se neshodují.";
		isValid = false;
	}

	return isValid;
}
