const schedulePopup = document.querySelector(".schedule_popup")

for (i = 0; i < scheduleCell.length - 1; i++){
    scheduleCell[i].addEventListener("click", schedulePopupFtn)
};

function schedulePopupFtn(){
    schedulePopup.style.display = "block"
}