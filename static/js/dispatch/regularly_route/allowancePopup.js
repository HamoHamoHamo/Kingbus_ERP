const referenceCloseBtn = document.querySelector(".referenceCloseBtn")
const referenceEditBtn = document.querySelector(".referenceEditBtn")
const popupAreaModules = document.querySelectorAll(".popupAreaModules")
const inputOutsourcingAllowance = document.querySelector(".inputOutsourcingAllowance")
const inputPrice = document.querySelector(".inputPrice")
const inputDriverAllowance = document.querySelector(".inputDriverAllowance")
const inputDriverAllowance2 = document.querySelector(".inputDriverAllowance2")
const inputMoney = document.querySelectorAll(".inputMoney")
const referenceDateInput = document.querySelector(".referenceDateInput")

for (i = 0; i < pricePopupArea.length; i++){
    pricePopupArea[i].addEventListener("click", referenceDatePopup)
};

function referenceDatePopup(){
    popupAreaModules[0].style.display = "block"
    inputPrice.value = priceValue
    inputDriverAllowance.value = driverAllowanceValue
    inputDriverAllowance2.value = driverAllowanceValue2
    inputOutsourcingAllowance.value = outsourcingAllowanceValue
}

Array.from(inputMoney).map(input => {
    input.value = input.value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    input.addEventListener("click", popupRemoveComma)
    input.addEventListener("blur", popupAddComma)
})


// inputPrice.addEventListener("click", popupRemoveComma)
// inputDriverAllowance.addEventListener("click", popupRemoveComma)
// inputOutsourcingAllowance.addEventListener("click", popupRemoveComma)
// inputPrice.addEventListener("blur", popupAddComma)
// inputDriverAllowance.addEventListener("blur", popupAddComma)
// inputOutsourcingAllowance.addEventListener("blur", popupAddComma)

function popupAddComma() {
    this.value = this.value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}

function popupRemoveComma() {
    this.value = this.value.replace(/\,/g, "")
}


referenceEditBtn.addEventListener("click", closeAndSaveInput)


function closeAndSaveInput(){
    if(referenceDateInput.value == ""){
        return alert("금액/수당 수정 기준일을 선택해 주세요")
    }
    pricePopupArea[0].innerText = inputPrice.value
    pricePopupArea[1].innerText = inputDriverAllowance.value
    popupAreaModules[0].style.display = "none"

    priceValue = inputPrice.value
    driverAllowanceValue = inputDriverAllowance.value
    driverAllowanceValue2 = inputDriverAllowance2.value
    outsourcingAllowanceValue = inputOutsourcingAllowance.value
}