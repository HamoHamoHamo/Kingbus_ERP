const searchAccount = document.querySelector(".searchAccount")
const accountCloseBtn = document.querySelector(".accountCloseBtn")

searchAccount.addEventListener("click", openAccounting)

function openAccounting(){
    popupAreaModules[2].style.display = "block"
}

accountCloseBtn.addEventListener("click", closeAccounting)
popupBgModules[2].addEventListener("click", closeAccounting)
SidemenuUseClose.addEventListener("click", closeAccounting)

function closeAccounting(){
    popupAreaModules[2].style.display = "none"
}