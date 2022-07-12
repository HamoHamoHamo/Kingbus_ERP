const openPopup = document.querySelector('.addState');
const popupAreaModules = document.querySelectorAll('.popupAreaModules');
const popupBgModules = document.querySelectorAll(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const popupCloseBtn = document.querySelectorAll(".PopupBtnBox div")
const openPopupToName = document.querySelectorAll(".tableBody td:nth-child(2)")
const editIcon = document.querySelectorAll(".managementDetailTableDataBox td svg")
const editStartDate = document.querySelectorAll(".managementDetailTableDataBox td:nth-child(2)")
const editEndDate = document.querySelectorAll(".managementDetailTableDataBox td:nth-child(3)")
const editContents = document.querySelectorAll(".managementDetailTableDataBox td:nth-child(4)")
const hrMemberListForm = document.querySelector(".hrMemberListForm")
const listCheckBox = document.querySelectorAll(".tableBody td:nth-child(1) input")



openPopup.addEventListener('click', hrRegistration);

function hrRegistration() {
    popupAreaModules[0].style.display = 'block'
}

for (i = 0; i < openPopupToName.length; i++) {
    openPopupToName[i].addEventListener('click', management);
}

function management() {
    popupAreaModules[1].style.display = 'block'
}


for (i = 0; i < popupBgModules.length; i++) {
    popupBgModules[i].addEventListener("click", closedcreatPopup)
}
SidemenuUseClose.addEventListener("click", closedcreatPopupToSideMEnu)
for (i = 0; i < popupCloseBtn.length; i++) {
    popupCloseBtn[i].addEventListener("click", closePopupBtn)
}

function closedcreatPopup() {
    for (i = 0; i < popupAreaModules.length; i++) {
        popupAreaModules[i].style.display = "none"
    }
}
function closedcreatPopupToSideMEnu() {
    for (i = 0; i < popupAreaModules.length; i++) {
        popupAreaModules[i].style.display = "none"
    }
}
function closePopupBtn() {
    for (i = 0; i < popupAreaModules.length; i++) {
        popupAreaModules[i].style.display = "none"
    }
}



/*수정*/
for (i = 0; i < editIcon.length; i++) {
    editIcon[i].addEventListener('click', useEdit)
}

function useEdit() {
    console.log(this.parentNode.parentNode.querySelector("td:nth-child(2) input"))
    this.parentNode.parentNode.querySelector("td:nth-child(2) input").disabled = false;
    this.parentNode.parentNode.querySelector("td:nth-child(2) input").style.border = '0.1rem solid #D2D2D2';
    this.parentNode.parentNode.querySelector("td:nth-child(3) input").disabled = false;
    this.parentNode.parentNode.querySelector("td:nth-child(3) input").style.border = '0.1rem solid #D2D2D2';
    this.parentNode.parentNode.querySelector("td:nth-child(4) input").disabled = false;
    this.parentNode.parentNode.querySelector("td:nth-child(4) input").style.border = '0.1rem solid #D2D2D2';
}


/*삭제*/
let checkCounte = false;

for (i = 0; i < listCheckBox.length; i++) {
    listCheckBox[i].addEventListener('change', checkingToDelete)
}

function checkingToDelete(){
    for (i = 0; i < listCheckBox.length; i++) {
      if (listCheckBox[i].checked) {
        checkCounte = true
      } else {
        checkCounte = false
      }
    }
    console.log(checkCounte)
}

hrMemberListForm.addEventListener('submit', activateDelete)

function activateDelete(e) {
    if (!checkCounte) {
        e.preventDefault()
        alert('삭제항 항목을 선택해 주세요.')
    }
}