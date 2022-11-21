const salaryItems = document.querySelectorAll(".salaryContainer .table-list_body-tr")
const amountCheckAll = document.querySelector(".amountCheckAll")

for (i = 0; i < salaryItems.length; i++){
    salaryItems[i].children[0].addEventListener("click", checkingChecker)
    salaryItems[i].children[1].addEventListener("click", checkingChecker)
    salaryItems[i].children[2].addEventListener("click", checkingChecker)
    salaryItems[i].children[3].addEventListener("click", checkingChecker)
    salaryItems[i].children[4].addEventListener("click", checkingChecker)
    salaryItems[i].children[5].addEventListener("click", checkingChecker)
    salaryItems[i].children[6].addEventListener("click", checkingChecker)
    salaryItems[i].children[7].addEventListener("click", checkingChecker)
    salaryItems[i].children[8].addEventListener("click", checkingChecker)
    salaryItems[i].children[11].addEventListener("click", checkingChecker)
};

function checkingChecker(){
    if(this.parentNode.children[0].children[0].checked){
        this.parentNode.children[0].children[0].checked = false
    }else{
        this.parentNode.children[0].children[0].checked = true
    }
    let checkCount = 0
    for (i = 0; i < amountCheck.length; i++){
        if(amountCheck[i].checked){
            checkCount++
        }
    };
    if(checkCount === amountCheck.length){
        amountCheckAll.checked = true
    }else{
        amountCheckAll.checked = false
    }
}

amountCheckAll.addEventListener("change", checkingAll)

function checkingAll(){
    if(this.checked){
        for (i = 0; i < amountCheck.length; i++){
            amountCheck[i].checked = true
        };
    }else{
        for (i = 0; i < amountCheck.length; i++){
            amountCheck[i].checked = false
        };
    }
}

for (i = 0; i < amountCheck.length; i++){
    amountCheck[i].addEventListener("click", checker)
};


function checker(e){
    e.stopPropagation()
    let checkCount = 0
    for (i = 0; i < amountCheck.length; i++){
        if(amountCheck[i].checked){
            checkCount++
        }
    };
    if(checkCount === amountCheck.length){
        amountCheckAll.checked = true
    }else{
        amountCheckAll.checked = false
    }
}