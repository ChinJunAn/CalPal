const openImageTabButton = document.getElementById("openWindowButton");

openImageTabButton.addEventListener("click", () => {
    const imageUrl = "static/picture.jpg";
    //const imageUrl = "../static/picture.jpg";
    const newTab = window.open(imageUrl, '_blank');
    if (newTab) {
        newTab.focus();
    } else {
        alert('Popup blocked. Please check your browser settings.');
    }
});
