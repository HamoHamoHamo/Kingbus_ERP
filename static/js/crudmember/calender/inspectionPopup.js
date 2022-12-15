const inspectionPopup = document.querySelector(".inspection_popup")
const inspectionPopupBtn = document.querySelector(".bus_inspection")
const inspectionLocation = document.querySelectorAll(".table_click_box")

inspectionPopupBtn.addEventListener("click", openInspectionPopup)

function openInspectionPopup(){
    inspectionPopup.style.display = "block"
}

for (i = 0; i < inspectionLocation.length; i++){
    inspectionLocation[i].addEventListener("click", locationInspection)
};

function locationInspection(){
    location.href= `vehicle/list?search=${this.children[1].innerText.split(" ")[1]}&select=vehicle`
}