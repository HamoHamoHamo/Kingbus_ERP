const amountInput = document.querySelectorAll(".amountInput")

for (i = 0; i < amountInput.length; i++){
    amountInput[i].addEventListener("change", amountValidation)
};

function amountValidation(){
    this.value = this.value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}

for (i = 0; i < amountInput.length; i++){
    amountInput[i].addEventListener("click", removeComma)
};

function removeComma(e){
    e.stopPropagation()
    this.value = this.value.replace(/\,/g, "");
}