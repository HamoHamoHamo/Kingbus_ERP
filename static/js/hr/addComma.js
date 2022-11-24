const salaryAddComma = document.querySelectorAll(".addComma")

function salaryComma(){
    for (i = 0; i < amountInput.length; i++){
        amountInput[i].value = amountInput[i].value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    };
    for (i = 0; i < salaryAddComma.length; i++){
        salaryAddComma[i].innerText = salaryAddComma[i].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    };
}

salaryComma()