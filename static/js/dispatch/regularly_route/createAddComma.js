amountComma[0].addEventListener("change", amountAddComma)
amountComma[1].addEventListener("change", amountAddComma)
amountComma[0].addEventListener("click", removeComma)
amountComma[1].addEventListener("click", removeComma)

function amountAddComma(){
    this.value = this.value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}

function removeComma(){
    this.value = this.value.replace(/\,/g, "")
}