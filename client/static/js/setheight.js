window.addEventListener('load', function() {
    const collectionOfInputBox = document.querySelectorAll('.inputBox');
    const loginBox = document.getElementById('box');
    
    if (collectionOfInputBox.length === 2) {
        loginBox.style.height = "450px";
    } else {
        loginBox.style.height = "610px";
    }
});