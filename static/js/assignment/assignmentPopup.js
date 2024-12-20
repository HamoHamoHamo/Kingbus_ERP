import { addEventClosePopup, closePopup } from "/static/js/common/popupCommon.js"
addEventClosePopup()

const popupAreaModules = document.querySelectorAll('.popupAreaModules')
const addPopupOpenBtn = document.querySelector('.addPopupOpenBtn')

addPopupOpenBtn.addEventListener("click", () => {
    popupAreaModules[0].style.display = "block"
})

