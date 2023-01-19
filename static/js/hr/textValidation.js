for (i = 0; i < amountInput.length; i++){
    amountInput[i].addEventListener("change", amountValidation)
};

function amountValidation(){
    this.value = this.value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    this.parentNode.parentNode.children[5].children[0].name = "base"
    this.parentNode.parentNode.children[6].children[0].name = "service"
    this.parentNode.parentNode.children[7].children[0].name = "position"
    this.parentNode.parentNode.children[8].children[0].name = "meal"
    if(this.parentNode.parentNode.children[15] === undefined){
        const hidden = document.createElement("input")
        hidden.setAttribute("type", "hidden")
        hidden.setAttribute("name", "id")
        hidden.setAttribute("value", this.parentNode.parentNode.children[0].children[0].value)
        this.parentNode.parentNode.appendChild(hidden)
    }    
}

for (i = 0; i < amountInput.length; i++){
    amountInput[i].addEventListener("click", removeComma)
};

function removeComma(e){
    e.stopPropagation()
    this.value = this.value.replace(/\,/g, "");
}


for (i = 0; i < amountInput.length; i++){
    amountInput[i].addEventListener("input", amountOnlyNum)
};

function amountOnlyNum(){
    let check = /^[0-9]+$/
    let regex = /[^0-9]/g;
    if(!check.test(this.value)){
        this.value = this.value.replace(regex, "")
    }
}



for (i = 0; i < amountInput.length; i++){
    amountInput[i].addEventListener("focusout", makeResult)
};

function makeResult(){
    let result = this.value.replace(/\,/g, "");
    targetInput = this
    remove0(result, targetInput)
}

function remove0(result, targetInput){
    if(result.length > 1){
        if(result[0] == 0){
            result = result.substr(1,)
            remove0(result, targetInput)
        }else{
            addComma(result, targetInput)
        }
    }
}

function addComma(result, targetInput){
    targetInput.value = result
    targetInput.value = targetInput.value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}