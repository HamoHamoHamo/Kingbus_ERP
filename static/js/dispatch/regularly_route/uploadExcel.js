const excelUpload = document.querySelector(".excelUpload")
const popupAreaModules = document.querySelector(".popupAreaModules")
const popupBgModules = document.querySelector(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const excelPopupCloseBtn = document.querySelector(".excelPopupCloseBtn")
const excelUploadFile = document.querySelector(".excelUploadFile")
const excelUploadFileText = document.querySelector(".excelUploadFileText")

excelUpload.addEventListener("click", openUploadPopup)

function openUploadPopup(){
    popupAreaModules.style.display = "block"
}

popupBgModules.addEventListener("click", closePopup)
SidemenuUseClose.addEventListener("click", closePopup)
excelPopupCloseBtn.addEventListener("click", closePopup)

function closePopup(){
    popupAreaModules.style.display = "none"
    excelUploadFile.value = ""
    excelUploadFileText.value = ""
}

excelUploadFile.addEventListener("change", fileUpload)

function fileUpload(){
    excelUploadFileText.value = excelUploadFile.files[0].name
}