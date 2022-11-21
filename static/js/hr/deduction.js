const deduction = document.querySelectorAll(".scrolling_table-list_body td:nth-child(11)")
const deductionPopup = document.querySelector(".deductionPopup")
const popupBgModulesDeduction = document.querySelector(".popupBgModulesDeduction")
const deductionCloseBtn = document.querySelector(".deductionCloseBtn")
for (i = 0; i < deduction.length; i++){
    deduction[i].addEventListener("click", openAddSalaryPopup)
};

function openAddSalaryPopup(){
    deductionPopup.style.display = "block"
}


popupBgModulesDeduction.addEventListener("click", closeAddSalaryPopup)
deductionCloseBtn.addEventListener("click", closeAddSalaryPopup)
SidemenuUseClose.addEventListener("click", closeAddSalaryPopup)

function closeAddSalaryPopup(){
    deductionPopup.style.display = "none"
}