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
const getTotal1 = document.querySelectorAll(".tableBody td:nth-child(3)")
const getTotal2 = document.querySelectorAll(".tableBody td:nth-child(4)")
const getTotal3 = document.querySelectorAll(".tableBody td:nth-child(5)")
const addComma1 = document.querySelectorAll(".tableBody td:nth-child(6)")
const addComma2 = document.querySelectorAll(".tableBody td:nth-child(7)")
const addComma3 = document.querySelectorAll(".tableBody td:nth-child(8)")
const addComma4 = document.querySelectorAll(".tableBody td:nth-child(9)")
const addComma5 = document.querySelectorAll(".tableBody td:nth-child(10)")
const PopupDataInputCeratePrice = document.querySelector(".PopupDataInputCeratePrice")
const detailTotal = document.querySelectorAll(".detailTotal td")


let selectingName = popupSelect.value
let renewal = false


//등록팝업 열기
openCrete.addEventListener("click", openCreatePopup)

function openCreatePopup() {
    popupAreaModules[0].style.display = "block"
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


// , 추가
PopupDataInputCeratePrice.addEventListener('change', addComma)

function addComma() {
    this.value = this.value.replace(/\,/g, "")
    this.value = this.value.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}



// , 추가, 단위추가
window.onload = function () {
    for (i = 0; i < addComma1.length; i++) {
        if (addComma1[i].innerText !== "") {
            addComma1[i].innerText = `${addComma1[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
        }
        if (addComma2[i].innerText !== "") {
            addComma2[i].innerText = `${addComma2[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
        }
        if (addComma3[i].innerText !== "") {
            addComma3[i].innerText = `${addComma3[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
        }
        if (addComma4[i].innerText !== "") {
            addComma4[i].innerText = `${addComma4[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
        }
        if (addComma5[i].innerText !== "") {
            addComma5[i].innerText = `${addComma5[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
        }
    }

    //합계 계산
    let getTotal1Count = "0"
    let getTotal2Count = "0"
    let getTotal3Count = "0"
    let addComma1Total = "0"
    let addComma2Total = "0"
    let addComma3Total = "0"
    let addComma4Total = "0"
    let addComma5Total = "0"
    for (i = 0; i < getTotal1.length; i++) {
        if (getTotal1[i].innerText !== "") {
            getTotal1Count = parseInt(getTotal1Count) + 1;
        }
        if (getTotal2[i].innerText !== "") {
            getTotal2Count = parseInt(getTotal2Count) + 1;
        }
        if (getTotal3[i].innerText !== "") {
            getTotal3Count = parseInt(getTotal3Count) + 1;
        }
        if (addComma1[i].innerText !== "") {
            addComma1Total = parseInt(addComma1Total) + parseInt(addComma1[i].innerText.replace(/[ㄱ-ㅎㅏ-ㅣ가-힣\,]/g, ""))
        }
        if (addComma2[i].innerText !== "") {
            addComma2Total = parseInt(addComma2Total) + parseInt(addComma2[i].innerText.replace(/[ㄱ-ㅎㅏ-ㅣ가-힣\,]/g, ""))
        }
        if (addComma3[i].innerText !== "") {
            addComma3Total = parseInt(addComma3Total) + parseInt(addComma3[i].innerText.replace(/[ㄱ-ㅎㅏ-ㅣ가-힣\,]/g, ""))
            console.log(addComma3Total)
        }
        if (addComma4[i].innerText !== "") {
            addComma4Total = parseInt(addComma4Total) + parseInt(addComma4[i].innerText.replace(/[ㄱ-ㅎㅏ-ㅣ가-힣\,]/g, ""))
        }
        if (addComma5[i].innerText !== "0원") {
            addComma5Total = parseInt(addComma5Total) + parseInt(addComma5[i].innerText.replace(/[ㄱ-ㅎㅏ-ㅣ가-힣\,]/g, ""))
        }
    }
    detailTotal[1].innerText = `${getTotal1Count}개`
    detailTotal[2].innerText = `${getTotal2Count}개`
    detailTotal[3].innerText = `${getTotal3Count}개`
    detailTotal[4].innerText = `${String(addComma1Total).replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
    detailTotal[5].innerText = `${String(addComma2Total).replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
    detailTotal[6].innerText = `${String(addComma3Total).replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
    detailTotal[7].innerText = `${String(addComma4Total).replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
    detailTotal[8].innerText = `${String(addComma5Total).replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`

    //기타 색 변화
    for (i = 0; i < addComma4.length; i++) {
        if (addComma4[i].title !== "") {
            addComma4[i].style.color = "#0069D9"
        }
    }
}


// , 추가
PopupDataInputPrice.addEventListener('change', addComma)

let onlyNumber = /[^0-9]/g;

function addComma(){
    this.value = this.value.replace(onlyNumber, "")
    this.value = this.value.replace(/\,/g,"")
    this.value = this.value.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

