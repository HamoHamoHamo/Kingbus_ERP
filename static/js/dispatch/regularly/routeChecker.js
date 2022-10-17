const checkAll = document.querySelector(".allChecker")
const check = document.querySelectorAll(".RouteListHBodyTr input[type=checkbox]")

// 전체 체크
checkAll.addEventListener("change", allCheck)

function allCheck() {
    if (this.checked) {
        for (i = 0; i < check.length; i++) {
            check[i].checked = true;
        }
    } else {
        for (i = 0; i < check.length; i++) {
            check[i].checked = false;
        }
    }
}


// 개별 체크
for (i = 0; i < check.length; i++) {
    check[i].addEventListener("change", checker)
}

function checker() {
    let checkCounter = 0;
    for (i = 0; i < check.length; i++) {
        if (check[i].checked) {
            checkCounter = checkCounter + 1
        }
    }
    if(checkCounter == check.length){
        checkAll.checked = true
    }else{
        checkAll.checked = false
    }
}