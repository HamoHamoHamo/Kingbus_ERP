const openCrete = document.querySelector(".addSalay")
const popupAreaModules = document.querySelector(".popupAreaModules")
const popupBgModules = document.querySelector(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const PopupCloseBtn = document.querySelector(".closeBtn")
const editePopupBtn = document.querySelector(".btnBox div")
const PopupTitle = document.querySelector(".PopupTitle")
const popupSelect = document.querySelector(".popupSelect")
const popupSelectOP = document.querySelectorAll(".popupSelect option")
const popupEntering = document.querySelector(".popupEntering")
const popupContainer = document.querySelector(".popupContainer")
const popupSelectOp = document.querySelectorAll(".popupSelect option")
const popupDate = document.querySelectorAll(".PopupDataInput")
const addComma1 = document.querySelectorAll(".tableBody td:nth-child(3)")
const addComma2 = document.querySelectorAll(".tableBody td:nth-child(4)")
const addComma3 = document.querySelectorAll(".tableBody td:nth-child(5)")
const addComma4 = document.querySelectorAll(".tableBody td:nth-child(6)")
const addComma5 = document.querySelectorAll(".tableBody td:nth-child(7)")
const PopupDataInputPrice = document.querySelector(".PopupDataInputPrice")


let selectingName = popupSelect.value
let renewal = false


//등록팝업 열기
openCrete.addEventListener("click", openCreatePopup)

function openCreatePopup() {
    popupAreaModules.style.display = "block"
}


//팝업닫기
popupBgModules.addEventListener("click", closePopup)
PopupCloseBtn.addEventListener("click", closePopup)
SidemenuUseClose.addEventListener("click", closePopup)

function closePopup() {
    PopupTitle.innerText = "급여등록"
    popupAreaModules.style.display = "none"
    popupDate[1].value = ""
}

//급여등록 입사일자
popupSelect.addEventListener('change', showEnteringDate)

function showEnteringDate() {
    for (i = 0; i < popupSelectOP.length; i++) {
        if (popupSelectOP[i].selected == true) {
            popupEntering.innerText = entering_date[popupSelectOP[i].value]
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
        if(confirm('정말로 내용을 덮어쓰시겠습니까?') == false)
        e.preventDefault()
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


// , 추가, 단위추가
window.onload = function () {
    for (i = 0; i < addComma1.length; i++) {
      addComma1[i].innerText = `${addComma1[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
      addComma2[i].innerText = `${addComma2[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
      addComma3[i].innerText = `${addComma3[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
      addComma4[i].innerText = `${addComma4[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
      addComma5[i].innerText = `${addComma5[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
    }
  }