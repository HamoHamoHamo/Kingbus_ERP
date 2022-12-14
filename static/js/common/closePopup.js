const popup = document.querySelectorAll(".basic_popup")
const popupBg = document.querySelectorAll(".basic_popup_bg")
const popupCloseBtn = document.querySelectorAll(".popup_btn-close")
const popupSidemenu = document.querySelector(".side_menu")

for (i = 0; i < popupBg.length; i++) {
    popupBg[i].addEventListener("click", () => closePopup(false, "nothing"))
};
for (i = 0; i < popupCloseBtn.length; i++) {
    popupCloseBtn[i].addEventListener("click", () => closePopup(false, "nothing"))
};


popupSidemenu.addEventListener("click", () => closePopup(false, "nothing"))


// 직원등록, 차량등록, 거래처등록 팝업에 dont_remove class 추가하기
function closePopup(when, open) {
    if (!when) {
        for (i = 0; i < popup.length; i++) {
            popup[i].style.display = "none"
            if (!popup[i].classList.contains(".dont_remove")) {
                const popupInpup = popup[i].querySelectorAll("input")
            }
        };
    } else {
        if (open === "id") {
            changePwPopup.style.display = "none"
        } else if (open === "pw") {
            changeIdPopup.style.display = "none"
        }
    }
}