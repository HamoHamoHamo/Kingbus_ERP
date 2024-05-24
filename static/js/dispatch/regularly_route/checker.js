const check = document.querySelectorAll(".driveDateBox input")
const checkbox = document.querySelectorAll(".RouteListBody input[type=checkbox]")
const allCheckbox = document.querySelector(".RouteListHeader input[type=checkbox]")


check[0].addEventListener("change", checkAll)

function checkAll(){
    if(check[0].checked){
        for(i=1; i<check.length; i++){
            check[i].checked = true
        }
    }else{
        for(i=1; i<check.length; i++){
            check[i].checked = false
        }
    }
}


for(i=1; i<check.length; i++){
    check[i].addEventListener("change", checkToAllcheck)
}

function checkToAllcheck(){
    if(check[1].checked == true && check[2].checked == true && check[3].checked == true && check[4].checked == true && check[5].checked == true && check[6].checked == true && check[7].checked == true){
        check[0].checked = true
    }else{
        check[0].checked = false
    }
}


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

