const referenceCloseBtn = document.querySelector(".referenceCloseBtn")
const referenceEditBtn = document.querySelector(".referenceEditBtn")
const popupAreaModules = document.querySelectorAll(".popupAreaModules")
const inputPrice = document.querySelector(".inputPrice")
const inputAllowance = document.querySelector(".inputAllowance")
const inputMoney = document.querySelectorAll(".inputMoney")
const referenceDateInput = document.querySelector(".referenceDateInput")

for (i = 0; i < pricePopupArea.length; i++){
    pricePopupArea[i].addEventListener("click", referenceDatePopup)
};

function referenceDatePopup(){
    popupAreaModules[0].style.display = "block"
    inputPrice.value = priceValue
    inputAllowance.value = allowanceValue

}

Array.from(inputMoney).map(input => {
    input.value = input.value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    input.addEventListener("click", popupRemoveComma)
    input.addEventListener("blur", popupAddComma)
})



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
    pricePopupArea[1].innerText = inputAllowance.value
    popupAreaModules[0].style.display = "none"

    priceValue = inputPrice.value
    allowanceValue = inputAllowance.value
}