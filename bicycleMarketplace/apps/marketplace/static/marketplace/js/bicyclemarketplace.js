function handleFileSelect(input) {
    if (input.files && input.files[0]) {
        previewURL = URL.createObjectURL(input.files[0]);
        imgPreviewElement = input.parentNode.parentNode.querySelector(' #picture_preview')
        if (imgPreviewElement.style.visibility = 'hidden') {
            imgPreviewElement.style.visibility = 'visible';
        }
        imgPreviewElement.src = previewURL;
    }
}
function bikeSelect(input) {
	// Checking if coming from /browse route
	if (/browse/.test(window.location.href)) {
    	window.location.href = '/bikes/' + input
    }
    // Checking if coming from /bikes route
    if (/bikes/.test(window.location.href)) {
    	window.location.href = '/bikes/update/' + input
    }
}

function modalShow(modalName) {
	let modal = document.getElementById("modal");
	let registerModal = document.getElementById("registerModal")
	let loginModal = document.getElementById("loginModal");

	modal.style.display = "block";
	
	if (modalName == "login" ) {
		registerModal.style.display = "none";
		loginModal.style.display = "block";
	} else{
		loginModal.style.display = "none";
		registerModal.style.display = "block";
	}

}

window.onclick = function(event) {
	let modal = document.getElementById("modal");
	if (event.target == modal) {
		modal.style.display = "none";
	}
}

function modalClose() {
	let modal = document.getElementById("modal");
	modal.style.display = "none";
}