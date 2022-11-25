const numberOnly = document.querySelectorAll(".numberOnly")

for (i = 0; i < numberOnly.length; i++){
    numberOnly[i].addEventListener("input", typeChecker)
    numberOnly[i].addEventListener("change", commaInclude)
    numberOnly[i].addEventListener("click", commaRemove)
};

function typeChecker(){
    this.value = this.value.replace(/[^0-9]/g,'');
}

function commaInclude(){
    this.value = this.value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}

function commaRemove(){
    this.value = this.value.replace(/\,/g, "")
}