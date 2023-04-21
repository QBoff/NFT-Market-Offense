const userLogin = document.querySelector('#login');
const emailEl = document.querySelector('#email');
const passwordEl = document.querySelector('#password');

const form = document.querySelector('#form');


const checkEmail = () => {
    let valid = false;
    const email = emailEl.value.trim();

    if (!isRequired(email)) {
        showError(emailEl, 'Email cannot be blank.');
    } else if (!isEmailValid(email)) {
        showError(emailEl, 'Email is not valid.')
    } else {
        // alert("Email валиден");
        valid = true;
    }

    if (!valid) alert("Email не валиден");
    return valid;
};


const checkPassword = () => {
    let valid = false;

    const password = passwordEl.value.trim();

    if (!isRequired(password)) {
        alert('Password cannot be blank.');
    } else if (!isPasswordSecure(password)) {
        alert('Password must has at least 8 characters that include at least 1 lowercase character, 1 uppercase characters, 1 number, and 1 special character in (!@#$%^&*)');
    } else {
        // alert("Все хорошо");
        valid = true;
    }

    return valid;
};

const checkOldPassword = () => {
    let valid = false;

    const password = oldPassword.value.trim();

    if (!isRequired(password)) {
        alert('Password cannot be blank.');
    } else if (!isPasswordSecure(password)) {
        alert('Password must has at least 8 characters that include at least 1 lowercase character, 1 uppercase characters, 1 number, and 1 special character in (!@#$%^&*)');
    } else {
        // alert("Все хорошо");
        valid = true;
    }

    return valid;
}

const isEmailValid = (email) => {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
};

const isPasswordSecure = (password) => {
    const re = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{8,})");
    return re.test(password);
};

const isRequired = value => value === '' ? false : true;

document.getElementById("update-btn").addEventListener('click', function (e) {
    // prevent the form from submitting

    e.preventDefault();
    // validate fields
    let isEmailValid = checkEmail(),
        isPasswordValid = checkPassword();

    let isFormValid = isPasswordValid && isEmailValid;


    if (!isFormValid) { } else {
        const oldPassword = prompt("Введите старый пароль: ");
        let isOldPasswordValid = isPasswordSecure(oldPassword.trim());

        if (isOldPasswordValid) {
            console.log(oldPassword);
            let input = document.createElement('input');
            input.setAttribute('type', 'hidden');
            input.setAttribute('value', oldPassword);
            input.setAttribute('id', 'oldPassword');
            input.setAttribute('name', 'oldPassword')
            form.appendChild(input);

            console.log(document.getElementById('email').value, document.getElementById('password').value, document.getElementById('oldPassword'));
            document.getElementById('form').submit();

            console.log("form was submitted");
        } else {
            alert("Старый пароль не валиден. Проверьте правильность его написания!");
        }
    }

});