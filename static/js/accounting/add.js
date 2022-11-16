const add = document.querySelectorAll(".add")
const additionalPopup = document.querySelector(".additionalPopup")
const addCloseBtn = document.querySelector(".addCloseBtn")
const popupBgModulesAdd = document.querySelector(".popupBgModulesAdd")

for (i = 0; i < add.length; i++){
    add[i].addEventListener("click", additionPopup)
};

function additionPopup(){
    additionalPopup.style.display = "block"
}




//팝업닫기
popupBgModulesAdd.addEventListener("click", closePopupAdd)
addCloseBtn.addEventListener("click", closePopupAdd)
SidemenuUseClose.addEventListener("click", closePopupAdd)


function closePopupAdd() {
    additionalPopup.style.display = "none"
}
