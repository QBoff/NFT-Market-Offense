window.addEventListener('load', function() {
    const collectionOfInputBox = document.querySelectorAll('.inputBox');
    const loginBox = document.getElementById('box');
    
    if (collectionOfInputBox.length === 3) {
        loginBox.style.height = "550px";
    } else {
        loginBox.style.height = "610px";
    }
});