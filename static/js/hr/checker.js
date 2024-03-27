const amountCheckAll = document.querySelector(".amountCheckAll")
const checkTd = document.querySelectorAll(".checkTd")

for (i = 0; i < checkTd.length; i++){
    checkTd[i].addEventListener("click", checkingChecker)
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