const amountProcessed = document.querySelectorAll(".depositCell td:nth-child(9)")
const amountProcessedCloseBtn = document.querySelector(".amountProcessedCloseBtn")
const amountProcessedTitle = document.querySelector(".amountProcessedTitle")

for (i = 0; i < amountProcessed.length; i++){
    amountProcessed[i].addEventListener("click", openPopup)
};

function openPopup(event){
    event.stopPropagation()
    popupAreaModules[1].style.display = "block"
    amountProcessedTitle.innerText = `[${this.parentNode.children[1].innerText}] 처리내역`
}

popupBgModules[1].addEventListener("click", closePopup)
SidemenuUseClose.addEventListener("click", closePopup)
amountProcessedCloseBtn.addEventListener("click", closePopup)

function closePopup(){
    popupAreaModules[1].style.display = "none"
}