const referenceCloseBtn = document.querySelector(".referenceCloseBtn")
const referenceEditBtn = document.querySelector(".referenceEditBtn")

for (i = 0; i < pricePopupArea.length; i++){
    pricePopupArea[i].addEventListener("click", referenceDatePopup)
};

function referenceDatePopup(){
    popupAreaModules[0].style.display = "block"
    inputPrice.value = pricePopupArea[0].innerText
    inputDriverAllowance.value = pricePopupArea[1].innerText
}

inputPrice.addEventListener("click", popupRemoveComma)
inputDriverAllowance.addEventListener("click", popupRemoveComma)
inputPrice.addEventListener("change", popupAddComma)
inputDriverAllowance.addEventListener("change", popupAddComma)


function popupAddComma() {
    this.value = this.value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}

function popupRemoveComma() {
    this.value = this.value.replace(/\,/g, "")
}



if(parms.has("id")){
    popupBgModules[1].addEventListener("click", referenceDateClose)
    SidemenuUseClose.addEventListener("click", referenceDateClose)
    referenceCloseBtn.addEventListener("click", referenceDateClose)
    referenceEditBtn.addEventListener("click", closeAndInput)
}

function referenceDateClose(){
    popupAreaModules[0].style.display = "none"
}



function closeAndInput(){
    pricePopupArea[0].innerText = inputPrice.value
    pricePopupArea[1].innerText = inputDriverAllowance.value
    popupAreaModules[0].style.display = "none"
}