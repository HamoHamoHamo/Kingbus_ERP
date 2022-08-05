const insurance = document.querySelectorAll(".tableBody .insuranceTable td:nth-child(1)")
const test = document.querySelectorAll(".tableBody .testTable td:nth-child(1)")
const popupAreaModules = document.querySelectorAll(".popupAreaModules")
const popupBgModules = document.querySelectorAll(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const dispatchCloseBtn = document.querySelectorAll(".PopupBtnBox div")
const insuranceVehicleNum = document.querySelector(".insuranceVehicleNum")
const insuranceEndDate = document.querySelector(".insuranceEndDate")
const testVehicleNum = document.querySelector(".testVehicleNum")
const testEndDate = document.querySelector(".testEndDate")
const fileNameBox = document.querySelector(".fileNameBox")
const fileDeletBtn = document.querySelector(".fileDeletBtn")
const sendToHidden = document.querySelectorAll(".sendToHidden")
const insuranceFile = document.querySelector("#insuranceFile")
const roundUnit = document.querySelectorAll(".insuranceTable td:nth-child(3)")
const priceUnit = document.querySelectorAll(".insuranceTable td:nth-child(4)")


//보험 수정창 열기
for (i = 0; i < insurance.length; i++) {
    insurance[i].addEventListener("click", openInsurance)
}

function openInsurance() {
    popupAreaModules[0].style.display = "block"
    insuranceVehicleNum.innerText = this.innerText
    insuranceEndDate.value = this.parentNode.childNodes[9].innerText
    if (insurance_list[this.className] == undefined) {
        fileNameBox.value = ""
    } else {
        fileNameBox.value = insurance_list[this.className]
    }
    sendToHidden[0].value = this.className;
}


//정기점검 수정창 열기
for (i = 0; i < test.length; i++) {
    test[i].addEventListener("click", openTest)
}

function openTest() {
    popupAreaModules[1].style.display = "block"
    testVehicleNum.innerText = this.innerText
    testEndDate.value = this.parentNode.childNodes[5].innerText.substr(0, 10)
    sendToHidden[1].value = this.className;
}


//팝업닫기
for (i = 0; i < 2; i++) {
    popupBgModules[i].addEventListener("click", closePopup)
    dispatchCloseBtn[i].addEventListener("click", closePopup)
}
SidemenuUseClose.addEventListener("click", closePopup)

function closePopup() {
    for (i = 0; i < 2; i++) {
        popupAreaModules[i].style.display = "none"
    }
}


//파일삭제
fileDeletBtn.addEventListener("click", deletFile)

function deletFile() {
    fileNameBox.value = ""
}

//파일명 변경
insuranceFile.addEventListener("change", changeFile)

function changeFile(){
    fileNameBox.value = insuranceFile.files[0].name
}




// , 추가, 단위추가
window.onload = function () {
    for (i = 0; i < roundUnit.length; i++) {
        if (roundUnit[i].innerText !== "") {
            roundUnit[i].innerText = `${roundUnit[i].innerText}회차`
        }
        if (priceUnit[i].innerText !== "") {
            priceUnit[i].innerText = `${priceUnit[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
        }
    }
  }