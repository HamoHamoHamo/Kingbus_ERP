const collectDateBox = document.querySelectorAll(".collectDateBox")
const routeSelect = document.querySelectorAll(".routeSelect")
const routeSelectAll = document.querySelector(".routeSelectAll")

for (i = 0; i < collectDateBox.length; i++){
    collectDateBox[i].children[0].addEventListener("click", selectCheck)
    collectDateBox[i].children[1].addEventListener("click", selectCheck)
    collectDateBox[i].children[2].addEventListener("click", selectCheck)
    collectDateBox[i].children[4].addEventListener("click", selectCheck)
    collectDateBox[i].children[5].addEventListener("click", selectCheck)
    collectDateBox[i].children[7].addEventListener("click", selectCheck)
    collectDateBox[i].children[8].addEventListener("click", selectCheckIf)
    collectDateBox[i].children[9].addEventListener("click", selectCheck)
    collectDateBox[i].children[10].addEventListener("click", selectCheck)
};

function selectCheck(e){
    e.stopPropagation()
    if(this.parentNode.children[0].children[0].checked){
        this.parentNode.children[0].children[0].checked = false
    }else{
        this.parentNode.children[0].children[0].checked = true
    }
    cheking(e)
}

function selectCheckIf(e){
    e.stopPropagation()
    if(this.innerText === ""){
        if(this.parentNode.children[0].children[0].checked){
            this.parentNode.children[0].children[0].checked = false
        }else{
            this.parentNode.children[0].children[0].checked = true
        }
        cheking(e)
    }
}

for (i = 0; i < routeSelect.length; i++){
    routeSelect[i].addEventListener("click", cheking)
};

function cheking(e){
    e.stopPropagation()
    let checkingCount = 0
    for (i = 0; i < routeSelect.length; i++){
        if(routeSelect[i].checked){
            checkingCount++
        }
    };
    if(checkingCount === routeSelect.length){
        routeSelectAll.checked = true
    }else{
        routeSelectAll.checked = false
    }
}

routeSelectAll.addEventListener("change", allChecker)

function allChecker(){
    if(this.checked){
        for (i = 0; i < routeSelect.length; i++){
            routeSelect[i].checked = true
        };
    }else{
        for (i = 0; i < routeSelect.length; i++){
            routeSelect[i].checked = false
        };
    }
}