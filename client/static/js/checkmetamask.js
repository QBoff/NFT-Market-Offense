let account = undefined;


window.addEventListener('load', function () {
    if (typeof window.ethereum !== "undefined") {

        ethereum
            .request({ method: "eth_requestAccounts" })
            .then((accounts) => {
                account = accounts[0];
                this.document.querySelector('.wallet').value = account;
            })

    } else {
        this.window.open("https://metamask.io/download/", "_blank");
    }
});