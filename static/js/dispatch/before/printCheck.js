const checker = document.querySelectorAll('.contentsCell input')
const checkAll = document.querySelector('.headerCell input')
const check = document.querySelectorAll('.contentsCell input')


let targetLink = ""
let checkerArray = []

function openDrivingPrint(url) {
    targetLink = `${url}${window.location.search}&id=${checkerArray}`
    if (targetLink == `${url}${window.location.search}&id=`) {
        alert("인쇄할 차량을 선택해 주세요.")
    } else {
        window.open(targetLink, "노선별A4", "width=1200, height=1600")
    }
}


for (i = 0; i < checker.length; i++) {
    checker[i].addEventListener('change', getCheckerId)
}


function getCheckerId() {
    if (this.checked == true) {
        checkerArray.push(this.parentNode.parentNode.className)
    } else {
        checkerArray = checkerArray.filter(current => current != this.parentNode.parentNode.className)
    }
}

checkAll.addEventListener('change', checkingAll)

function checkingAll() {
    if (checkAll.checked) {
        for (i = 0; i < check.length; i++) {
            check[i].checked = true
            checkerArray.push( check[i].parentNode.parentNode.className)
        }
    }else{
        for (i = 0; i < check.length; i++) {
            check[i].checked = false
            checkerArray = checkerArray.filter(current => current != check[i].parentNode.parentNode.className)
        }
    }
}