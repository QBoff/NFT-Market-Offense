window.addEventListener('load', function() {
    if (window.ethereum) {
        console.log("Ethereum support is available");

        if (window.ethereum.isMetaMask) {
            console.log("MetaMask has been installed");
        } else {
            console.log("Please install MetaMask");
        }
    } else {
        console.log("You have not any kind of MetaMask support");
    }
})