const editPopupCloseBtn = document.querySelector(".editPopupCloseBtn")

for (i = 0; i < depositCell.length; i++){
    depositCell[i].addEventListener("click", editPopup)
};

function editPopup(){
    popupAreaModules[2].style.display = "block"
}

popupBgModules[2].addEventListener("click", closePopupEdit)
SidemenuUseClose.addEventListener("click", closePopupEdit)
editPopupCloseBtn.addEventListener("click", closePopupEdit)

function closePopupEdit(){
    popupAreaModules[2].style.display = "none"
}