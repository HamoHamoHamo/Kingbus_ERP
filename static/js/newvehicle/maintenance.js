const createBtn = document.querySelector(".maintenanceCreateBtn")
const popupAreaModules = document.querySelector(".popupAreaModules")
const popupBgModules = document.querySelector(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const maintenanceCloseBtn = document.querySelector(".maintenanceCloseBtn")
const hiddenId = document.querySelector(".popupArticleDouble input[type=hidden]")


createBtn.addEventListener("click", openMaintenance)

function openMaintenance() {
    popupAreaModules.style.display = "block"
    // hiddenId = window.location.search.replace("busid=")[1]
}

popupBgModules.addEventListener("click", closePopup)
SidemenuUseClose.addEventListener("click", closePopup)
maintenanceCloseBtn.addEventListener("click", closePopup)

function closePopup() {
    popupAreaModules.style.display = "none"
}


// window.onload = function () {
//     if(window.location.search == ""){
//         createBtn.style.display = "none"
//     }
// }