// regularly_connect_list.html 기준으로 만듦

let commonPopupAreaModules = document.querySelectorAll('.popupAreaModules')

const addClosePopupEvent = () => {
    const commonPopupBgModules = document.querySelector(".popupBgModules")
    const commonSidemenuUseClose = document.querySelector(".Sidemenu")

    commonPopupBgModules.addEventListener('click', closePopup)
    commonSidemenuUseClose.addEventListener('click', closePopup)
    console.log("add close popup event")
}

const closePopup = () => {
    Array.from(commonPopupAreaModules).map((popupAreaModule) => {
        popupAreaModule.style.display = "none"
    })
}



export { addClosePopupEvent, closePopup }