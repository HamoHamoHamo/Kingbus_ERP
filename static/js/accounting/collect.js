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


//팝업열기
for (i = 0; i < collectPopupOpen.length; i++) {
    collectPopupOpen[i].addEventListener('click', openPopup)
}

function openPopup() {
    popupAreaModules.style.display = "block"
    PopupData[0].innerText = regDatas[this.parentNode.className].departure
    PopupData[1].innerText = regDatas[this.parentNode.className].bus_cnt
    PopupData[2].innerText = regDatas[this.parentNode.className].arrival
    PopupData[3].innerText = regDatas[this.parentNode.className].bus_type
    PopupData[4].innerText = `${regDatas[this.parentNode.className].departure_date} ~ ${regDatas[this.parentNode.className].arrival_date}`
    PopupData[5].innerText = regDatas[this.parentNode.className].contract_status
    PopupData[6].innerText = regDatas[this.parentNode.className].cost_type
    PopupData[7].innerText = regDatas[this.parentNode.className].references
    PopupData[8].innerText = regDatas[this.parentNode.className].customer
    PopupData[9].innerText = regDatas[this.parentNode.className].customer_phone
    PopupData[10].innerText = regDatas[this.parentNode.className].price
    PopupData[11].innerText = regDatas[this.parentNode.className].deposit_status
    PopupData[12].innerText = regDatas[this.parentNode.className].deposit_date
    PopupData[13].innerText = regDatas[this.parentNode.className].bill_date
    PopupData[14].innerText = regDatas[this.parentNode.className].collection_type
    PopupData[15].innerText = regDatas[this.parentNode.className].driver_allowance
    if (regDatas[this.parentNode.className].payment_method == "y") {
        PopupData[16].innerText = "선지급"
    } else {
        PopupData[16].innerText = "x"
    }
    if (regDatas[this.parentNode.className].VAT == "y") {
        PopupData[17].innerText = "포함"
    } else {
        PopupData[17].innerText = "x"
    }
    sendToHidden.value = this.parentNode.parentNode.className;
    PopupDataInputPrice.value = regDatas[this.parentNode.className].collection_amount
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