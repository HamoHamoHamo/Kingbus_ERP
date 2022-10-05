const allChecker = document.querySelector(".documentTableHeader input")
const groupChecker = document.querySelectorAll(".groupCheck")
const fileChecker = document.querySelectorAll(".fileCheck")
const file = document.querySelectorAll(".documentContentsTableTbody td:nth-child(2)")




// 전체선택
allChecker.addEventListener("change", makeAllCheck)

function makeAllCheck() {
    if (this.checked) {
        for (i = 0; i < groupChecker.length; i++) {
            groupChecker[i].checked = true
        }
        for (i = 0; i < fileChecker.length; i++) {
            fileChecker[i].checked = true
        }
    } else {
        for (i = 0; i < groupChecker.length; i++) {
            groupChecker[i].checked = false
        }
        for (i = 0; i < fileChecker.length; i++) {
            fileChecker[i].checked = false
        }
    }
}




// 그룹선택
for (i = 0; i < groupChecker.length; i++) {
    groupChecker[i].addEventListener("change", makeGroupCheck)
}

function makeGroupCheck() {
    if (this.checked) {
        // 그룹 전체선택시 하위 체크박스와 연동
        for (i = 0; i < fileChecker.length; i++) {
            if (fileChecker[i].classList.contains(`${this.classList[1]}`)) {
                fileChecker[i].checked = true
            }
        }
        // 그룹 전체선택시 최상단 체크박스와 연동
        let groupCheckCount = []
        for (i = 0; i < groupChecker.length; i++) {
            if (groupChecker[i].checked) {
                groupCheckCount.push(groupChecker[i])
            }
        }
        if (groupChecker.length === groupCheckCount.length) {
            allChecker.checked = true
        }
    } else {
        // 그룹 전체선택시 하위 체크박스와 연동
        for (i = 0; i < fileChecker.length; i++) {
            if (fileChecker[i].classList.contains(`${this.classList[1]}`)) {
                fileChecker[i].checked = false
            }
        }
        // 그룹 전체선택시 최상단 체크박스와 연동
        let groupCheckCount = []
        for (i = 0; i < groupChecker.length; i++) {
            if (groupChecker[i].checked) {
                groupCheckCount.push(groupChecker[i])
            }
        }
        if (groupChecker.length !== groupCheckCount.length) {
            allChecker.checked = false
        }
    }
}

for (i = 0; i < fileChecker.length; i++) {
    fileChecker[i].addEventListener("change", makeCheck)
}

function makeCheck() {
}

for(i=0; i<file.length; i++){
    file[i].addEventListener("click", checkLink)
}

function checkLink(){
    if(this.parentNode.children[0].children[0].checked == false){
        this.parentNode.children[0].children[0].checked = true
    }else{
        this.parentNode.children[0].children[0].checked = false
    }

    
    if (this.parentNode.children[0].children[0].checked) {
        // 파일선택시 해당 그룹 체크박스와 연동
        const oneGroup = document.querySelectorAll(`.${this.parentNode.children[0].children[0].classList[1]}`)
        let checkCount = []
        for (i = 0; i < oneGroup.length; i++) {
            if (oneGroup[i].checked) {
                checkCount.push(oneGroup[i])
            }
        }
        if ((oneGroup.length - 1) === checkCount.length) {
            for (i = 0; i < groupChecker.length; i++) {
                if (groupChecker[i].classList.contains(`${this.parentNode.children[0].children[0].classList[1]}`)) {
                    groupChecker[i].checked = true
                }
            }
        }
        // 파일선택시 최상위 체크박스 연동
        let groupCheckCount = []
        for (i = 0; i < groupChecker.length; i++) {
            if (groupChecker[i].checked) {
                groupCheckCount.push(groupChecker[i])
            }
        }
        if (groupCheckCount.length === groupChecker.length) {
            allChecker.checked = true
        }
    } else {
        // 파일선택시 해당 그룹 체크박스와 연동
        const oneGroup = document.querySelectorAll(`.${this.parentNode.children[0].children[0].classList[1]}`)
        if (oneGroup[0].checked) {
            oneGroup[0].checked = false
        }
        if (allChecker.checked) {
            allChecker.checked = false
        }
    }
}