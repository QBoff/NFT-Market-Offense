/**
 * 
 * @param {String} inputId 
 */
function changeReadOnly(inputId) {
    document.getElementById(inputId).removeAttribute('readonly');
}


const updateLogin = document.getElementById('updatelogin');
const updateEmail = document.getElementById('updateemail');
const updatePassword = document.getElementById('updatepassword');
const updateWallet = document.getElementById('updatewallet');

updateLogin.onclick = changeReadOnly('login');
updateEmail.onclick = changeReadOnly('email');
updatePassword.onclick = changeReadOnly('password');
updateWallet.onclick = changeReadOnly('wallet');
