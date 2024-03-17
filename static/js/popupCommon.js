// regularly_connect_list.html 기준으로 만듦

let commonPopupAreaModules = document.querySelectorAll('.popupAreaModules')

const addClosePopupEvent = () => {
    const commonPopupBgModules = document.querySelectorAll(".popupBgModules")
    const commonSidemenuUseClose = document.querySelector(".Sidemenu")
    const popupCloseBtn = document.querySelectorAll(".popupCloseBtn")

    if (popupCloseBtn) {
        Array.from(popupCloseBtn).map(btn => {
            btn.addEventListener('click', closePopup)
        })
    }
    Array.from(commonPopupBgModules).map(bg => {
        bg.addEventListener('click', closePopup)
    })
    commonSidemenuUseClose.addEventListener('click', closePopup)
    console.log("add close popup event")
}

const closePopup = () => {
    Array.from(commonPopupAreaModules).map((popupAreaModule) => {
        popupAreaModule.style.display = "none"
    })
}

addClosePopupEvent()

// export { addClosePopupEvent, closePopup }