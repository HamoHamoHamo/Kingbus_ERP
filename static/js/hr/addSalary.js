const addSalarly = document.querySelectorAll(".scrolling_table-list_body td:nth-child(10)")
const addSalaryPopup = document.querySelector(".addSalaryPopup")
const popupBgModulesAddSalary = document.querySelector(".popupBgModulesAddSalary")
const addSalaryCloseBtn = document.querySelector(".addSalaryCloseBtn")
const SidemenuUseClose = document.querySelector(".Sidemenu")

for (i = 0; i < addSalarly.length; i++){
    addSalarly[i].addEventListener("click", openAddSalaryPopup)
};

function openAddSalaryPopup(){
    addSalaryPopup.style.display = "block"
}


popupBgModulesAddSalary.addEventListener("click", closeAddSalaryPopup)
addSalaryCloseBtn.addEventListener("click", closeAddSalaryPopup)
SidemenuUseClose.addEventListener("click", closeAddSalaryPopup)

function closeAddSalaryPopup(){
    addSalaryPopup.style.display = "none"
}