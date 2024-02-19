let params = new URLSearchParams(location.search)

if (!params.has("id")) {
    amountComma[0].addEventListener("change", amountAddComma)
    amountComma[1].addEventListener("change", amountAddComma)
    amountComma[0].addEventListener("click", removeComma)
    amountComma[1].addEventListener("click", removeComma)
}

function amountAddComma() {
    this.innerText = this.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}

function removeComma() {
    this.innerText = this.innerText.replace(/\,/g, "")
}