const deleteAllChecker = document.querySelector(".deleteAllChecker")
const deleteChecker = document.querySelectorAll(".deleteChecker")
const clientItem = document.querySelectorAll(".table-list_body-tr")

deleteAllChecker.addEventListener("change", deleteAllChecking)

function deleteAllChecking(){
    if(deleteAllChecker.checked){
        for (i = 0; i < deleteChecker.length; i++){
            deleteChecker[i].checked = true
        };
    }else{
        for (i = 0; i < deleteChecker.length; i++){
            deleteChecker[i].checked = false
        };
    }
}


for (i = 0; i < deleteChecker.length; i++){
    deleteChecker[i].addEventListener("click", deleteChecking)
};

function deleteChecking(e){
    e.stopPropagation()
    let deleteCount = 0
    for (i = 0; i < deleteChecker.length; i++){
        if(deleteChecker[i].checked){
            deleteCount++
        }
    };
    if(deleteChecker.length === deleteCount){
        deleteAllChecker.checked = true
    }else{
        deleteAllChecker.checked = false
    }
}


for (i = 0; i < clientItem.length; i++){
    clientItem[i].addEventListener("click", deleteCheckingForTr)
};

function deleteCheckingForTr(){
    let deleteCount = 0
    if(this.children[0].children[0].checked){
        this.children[0].children[0].checked = false
    }else{
        this.children[0].children[0].checked = true
    }
    for (i = 0; i < deleteChecker.length; i++){
        if(deleteChecker[i].checked){
            deleteCount++
        }
    };
    if(deleteChecker.length === deleteCount){
        deleteAllChecker.checked = true
    }else{
        deleteAllChecker.checked = false
    }
}