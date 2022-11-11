allChecker.addEventListener("change", allChecking)

let selectArr = []

function allChecking() {
    selectArr = []
    if (allChecker.checked) {
        for (i = 0; i < checker.length; i++) {
            checker[i].checked = true
            selectArr.push(i)
        };
    } else {
        for (i = 0; i < checker.length; i++) {
            checker[i].checked = false
            selectArr = []
        };
    }
    totalSelecting(selectArr)
}

for (i = 0; i < checker.length; i++) {
    checker[i].addEventListener("click", checking)
};

function checking(event) {
    event.stopPropagation()
    selectArr = []
    let checkCount = 0
    for (i = 0; i < checker.length; i++) {
        if (checker[i].checked) {
            checkCount++
            selectArr.push(i)
        }
    };
    if (checkCount == checker.length) {
        allChecker.checked = true
    } else {
        allChecker.checked = false
    }
    totalSelecting(selectArr)
}


for (i = 0; i < depositCell.length; i++){
    depositCell[i].children[0].addEventListener("click", checkboxCehck)
};

function checkboxCehck(e){
    event.stopPropagation()
    if(this.children[0].checked){
        this.children[0].checked = false;
    }else{
        this.children[0].checked = true;
    }
    checking(event)
}