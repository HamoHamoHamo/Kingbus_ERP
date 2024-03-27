for (i = 0; i < amountInput.length; i++){
    amountInput[i].addEventListener("change", amountValidation)
};

function amountValidation(){
    const tr = this.parentNode.parentNode

    this.value = this.value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    tr.querySelector('.salaryOvertimeAllowance') ? tr.querySelector('.salaryOvertimeAllowance').name = 'overtime' : null
    tr.querySelector('.salaryBase') ? tr.querySelector('.salaryBase').name = 'base' : null
    tr.querySelector('.salaryServiceAllowance') ? tr.querySelector('.salaryServiceAllowance').name = 'service' : null
    tr.querySelector('.salaryAnnualAllowance') ? tr.querySelector('.salaryAnnualAllowance').name = 'annual' : null
    tr.querySelector('.salaryPerformanceAllowance') ? tr.querySelector('.salaryPerformanceAllowance').name = 'performance' : null
    tr.querySelector('.salaryMeal') ? tr.querySelector('.salaryMeal').name = 'meal' : null

    if(tr.querySelector('.hiddenId') == undefined){
        const hidden = document.createElement("input")
        hidden.setAttribute("class", "hiddenId")
        hidden.setAttribute("type", "hidden")
        hidden.setAttribute("name", "id")
        hidden.setAttribute("value", tr.children[0].children[0].value)
        tr.appendChild(hidden)
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