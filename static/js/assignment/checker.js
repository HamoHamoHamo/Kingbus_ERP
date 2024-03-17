const checkbox = document.querySelectorAll(".RouteListBody input[type=checkbox]")
const allCheckbox = document.querySelector(".RouteListHeader input[type=checkbox]")

for (i = 0; i < checkbox.length; i++){
    checkbox[i].addEventListener('change', deletecheck)
};

function deletecheck(e){
    e.stopPropagation()
    let checkCount = 0
    for (i = 0; i < checkbox.length; i++){
        if(checkbox[i].checked){
            checkCount++ 
        }
    };
    if(checkbox.length === checkCount){
        allCheckbox.checked = true
    }else{
        allCheckbox.checked = false
    }
}

allCheckbox.addEventListener("change", allDeleteCheck)

function allDeleteCheck(){
    if(this.checked){
        for (i = 0; i < checkbox.length; i++){
            checkbox[i].checked = true
        };
    }else{
        for (i = 0; i < checkbox.length; i++){
            checkbox[i].checked = false
        };
    }
}