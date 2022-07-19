const openCrete = document.querySelector(".addSalay")
const popupAreaModules = document.querySelectorAll(".popupAreaModules")
const popupBgModules = document.querySelectorAll(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const PopupCloseBtn = document.querySelectorAll(".PopupBtnBox div")
const editePopupBtn = document.querySelector(".btnBox div")
const salaryForm = document.querySelector(".salaryForm")
const listCheckBox = document.querySelectorAll(".tableBody td:nth-child(1) input")
const popupSelect = document.querySelector(".popupSelect")
const popupSelectOP = document.querySelectorAll(".popupSelect option")
const popupSelectEditOP = document.querySelectorAll(".popupSelectEdit option")
const popupEntering = document.querySelectorAll(".popupEntering")
const editSalay = document.querySelectorAll(".tableBody td:nth-child(12)")
const popupContainer = document.querySelector(".popupContainer")
const popupSelectOp = document.querySelectorAll(".popupSelect option")
const popupDate = document.querySelectorAll(".PopupDataInput")
const PopupDataInputDate = document.querySelector(".PopupDataInputDate")
const PopupDataInputPrice = document.querySelector(".PopupDataInputPrice")
const PopupDataInputBlanck = document.querySelector(".PopupDataInputBlanck")
const sendToHidden = document.querySelector(".sendToHidden")


let selectingName = popupSelect.value
let renewal = false


//등록팝업 열기
openCrete.addEventListener("click", openCreatePopup)

function openCreatePopup() {
    popupAreaModules[0].style.display = "block"
    createBtn.style.display = "flex"
    editBtn.style.display = "none"
}


//팝업닫기
for (i = 0; i < 2; i++) {
    popupBgModules[i].addEventListener("click", closePopup)
    PopupCloseBtn[i].addEventListener("click", closePopup)
}
SidemenuUseClose.addEventListener("click", closePopup)

function closePopup() {
    popupAreaModules[0].style.display = "none"
    popupAreaModules[1].style.display = "none"
    popupDate[1].value = ""
}


/*삭제*/
let checkCounte = false;

for (i = 0; i < listCheckBox.length; i++) {
    listCheckBox[i].addEventListener('change', checkingToDelete)
}

function checkingToDelete() {
    checkCounte = false
    for (i = 0; i < listCheckBox.length; i++) {
        if (listCheckBox[i].checked) {
            checkCounte = true
        }
    }
    console.log(checkCounte)
}

salaryForm.addEventListener('submit', activateDelete)

function activateDelete(e) {
    if (!checkCounte) {
        e.preventDefault()
        alert('삭제할 항목을 선택해 주세요.')
    } else {
        if (confirm('정말로 삭제하시겠습니까?') == false) {
            e.preventDefault()
        }
    }
}


//수정팝업 열기
for (i = 0; i < editSalay.length; i++) {
    editSalay[i].addEventListener("click", openEditPopup)
}

function openEditPopup(e) {
    if (this.innerText !== "") {
        popupAreaModules[1].style.display = "block"
        for (i = 0; i < popupSelectEditOP.length; i++) {
            if (popupSelectEditOP[i].value == data[this.className].member_id) {
                popupSelectEditOP[i].selected = true;
            }
        }
        popupEntering[1].innerText = data[this.className].entering_date
        PopupDataInputDate.value = data[this.className].date
        PopupDataInputPrice.value = data[this.className].price
        PopupDataInputBlanck.value = data[this.className].remark
        sendToHidden.value = this.className
    }
}



//급여등록 입사일자
popupSelect.addEventListener('change', showEnteringDate)

function showEnteringDate() {
    for (i = 0; i < popupSelectOP.length; i++) {
        if (popupSelectOP[i].selected == true) {
            popupEntering[0].innerText = entering_date[popupSelectOP[i].value]
            selectingName = popupSelectOp[i].value
        }
    }
    dateCheck()
}



popupDate[1].addEventListener('change', callCheck)

function callCheck() {
    dateCheck()
}


//같은날짜 확인
function dateCheck() {
    renewal = false;
    if (additional[selectingName].indexOf(popupDate[1].value) == 0) {
        renewal = true;
    }
}

//중복일자

popupContainer.addEventListener('submit', createSalay)

function createSalay(e) {
    if (renewal) {
        if (confirm('정말로 내용을 덮어쓰시겠습니까?') == false)
            e.preventDefault()
    }
}