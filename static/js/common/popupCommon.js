// regularly_connect_list.html 기준으로 만듦

let commonPopupAreaModules = document.querySelectorAll('.popupAreaModules')

// popupBgModules, Sidemenu, popupCloseBtn 클릭 시 팝업 닫힘
const addEventClosePopup = () => {
    const commonPopupBgModules = document.querySelectorAll(".popupBgModules")
    const commonSidemenuUseClose = document.querySelector(".Sidemenu")
    const popupCloseBtn = document.querySelectorAll(".popupCloseBtn")
    console.log("GGG", popupCloseBtn)
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

class ClosePopup {
    static areaModules = document.querySelectorAll('.popupAreaModules')
    static bgModules = document.querySelectorAll(".popupBgModules")
    static sideMenu = document.querySelector(".Sidemenu")
    static closeBtn = document.querySelectorAll(".popupCloseBtn")

    static closePopup() {
        Array.from(this.areaModules).forEach(areaModule => areaModule.style.display = "none");
    }

    static addClosePopupEvent() {
        if (this.closeBtn) {
            Array.from(this.closeBtn).forEach(btn => btn.addEventListener('click', closePopup));
        }
        if (this.bgModules) {
            Array.from(this.bgModules).forEach(bg => bg.addEventListener('click', closePopup));
        }
        this.sideMenu?.addEventListener('click', closePopup);
        console.log("add close popup event");
    }

    set areaModules(areaModules) {
        this.areaModules = areaModules;
    }
    
    set bgModules(bgModules) {
        this.bgModules = bgModules;
    }
    
    set sideMenu(sideMenu) {
        this.sideMenu = sideMenu;
    }

    set closeBtn(closeBtn) {
        this.closeBtn = closeBtn;
    }
}

export { addEventClosePopup, closePopup, ClosePopup }