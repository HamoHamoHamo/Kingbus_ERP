const collectPopupOpen = document.querySelectorAll(".popupOpenBtn")
const popupAreaModules = document.querySelector(".popupAreaModules")
const popupBgModules = document.querySelector(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const closeBtnCollect = document.querySelector(".closeBtn")
const PopupData = document.querySelectorAll(".PopupData")
const sendToHidden = document.querySelector(".sendToHidden")
const PopupDataInputPrice = document.querySelector(".PopupDataInputPrice")
const PopupDataInputDate = document.querySelector(".PopupDataInputDate")
const PopupDataInputEditer = document.querySelector(".PopupDataInputEditer")
const phoneNum = document.querySelectorAll(".phoneNum")
const addComma1 = document.querySelectorAll(".tableBody td:nth-child(4)")
const addComma2 = document.querySelectorAll(".tableBody td:nth-child(9)")


//팝업열기
for (i = 0; i < collectPopupOpen.length; i++) {
    collectPopupOpen[i].addEventListener('click', openPopup)
}

function openPopup() {
    popupAreaModules.style.display = "block"
    PopupData[1].innerText = regDatas[this.parentNode.className].departure
    PopupData[2].innerText = regDatas[this.parentNode.className].bus_cnt
    PopupData[3].innerText = regDatas[this.parentNode.className].arrival
    PopupData[4].innerText = regDatas[this.parentNode.className].bus_type
    PopupData[5].innerText = `${regDatas[this.parentNode.className].departure_date} ~ ${regDatas[this.parentNode.className].arrival_date}`
    PopupData[6].innerText = regDatas[this.parentNode.className].contract_status
    PopupData[7].innerText = regDatas[this.parentNode.className].cost_type
    PopupData[8].innerText = regDatas[this.parentNode.className].references
    PopupData[9].innerText = regDatas[this.parentNode.className].customer
    PopupData[10].innerText = regDatas[this.parentNode.className].customer_phone
    PopupData[11].innerText = regDatas[this.parentNode.className].price
    PopupData[12].innerText = regDatas[this.parentNode.className].deposit_status
    PopupData[13].innerText = regDatas[this.parentNode.className].deposit_date
    PopupData[14].innerText = regDatas[this.parentNode.className].bill_date
    PopupData[15].innerText = regDatas[this.parentNode.className].collection_type
    PopupData[16].innerText = regDatas[this.parentNode.className].driver_allowance
    if (regDatas[this.parentNode.className].payment_method == "y") {
        PopupData[17].innerText = "선지급"
    } else {
        PopupData[17].innerText = "x"
    }
    if (regDatas[this.parentNode.className].VAT == "y") {
        PopupData[18].innerText = "포함"
    } else {
        PopupData[18].innerText = "x"
    }
    sendToHidden.value = this.parentNode.parentNode.className;
    PopupDataInputPrice.value = regDatas[this.parentNode.className].collection_amount.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    PopupDataInputDate.value = regDatas[this.parentNode.className].collection_date
    PopupDataInputEditer.value = regDatas[this.parentNode.className].collection_creator
}


//팝업닫기
popupBgModules.addEventListener("click", closePopup)
closeBtnCollect.addEventListener("click", closePopup)
SidemenuUseClose.addEventListener("click", closePopup)

function closePopup() {
    popupAreaModules.style.display = "none"
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
    for (i = 0; i < phoneNum.length; i++) {
        if (phoneNum[i].innerText !== "") {
            phoneNum[i].innerText = phoneNum[i].innerText.replace(/^(\d{2,3})(\d{3,4})(\d{4})$/, `$1-$2-$3`)
        }
        if (addComma1[i].innerText !== "") {
            addComma1[i].innerText = `${addComma1[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
        }
        if (addComma2[i].innerText !== "") {
            addComma2[i].innerText = `${addComma2[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
        }
        if (collectPopupOpen[i].innerText !== "0") {
            collectPopupOpen[i].innerText = `${collectPopupOpen[i].innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
        }else{
            collectPopupOpen[i].innerText = "0"
        }
    }
}