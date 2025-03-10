function addMoreImages() {
	const newInput = document.createElement("input");
	newInput.type = "file";
	newInput.className = "form-control mt-2";
	newInput.name = "pictures";
	newInput.accept = "image/*";
	document.getElementById("fileError").before(newInput);
}
