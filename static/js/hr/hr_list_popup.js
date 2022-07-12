const openPopup = document.querySelector('.addPeople');
const popupAreaModules = document.querySelectorAll('.popupAreaModules');
const popupBgModules = document.querySelectorAll(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const popupCloseBtn = document.querySelectorAll(".PopupBtnBox div")
const checkBox = document.querySelectorAll(".tableBody td:nth-child(1) input")
const hrMemberListForm = document.querySelector(".hrMemberListForm")
const editMember = document.querySelectorAll(".tableBody td:nth-child(2)")
const hrName = document.querySelector(".hrName")
const hrRole = document.querySelectorAll(".hrRole option")
const hrEntering = document.querySelector(".hrEntering")
const hrLicense = document.querySelector(".hrLicense")
const hrPhone = document.querySelector(".hrPhone")
const hrBirth = document.querySelector(".hrBirth")
const hrAddress = document.querySelector(".hrAddress")
const sendToHidden = document.querySelector(".sendToHidden")

for (i = 0; i < editMember.length; i++) {
  editMember[i].addEventListener('click', openDeitPopup)
}

function openDeitPopup() {
  popupAreaModules[1].style.display = 'block'
  hrName.value = regDatas[this.className].name;
  for (i = 0; i < hrRole.length; i++) {
    if (hrRole[i].innerText == regDatas[this.className].role) {
      hrRole[i].selected = true;
    }
  }
  hrEntering.value = regDatas[this.className].entering_date;
  hrLicense.value = regDatas[this.className].license_number;
  hrPhone.value = regDatas[this.className].phone_num;
  hrBirth.value = regDatas[this.className].birthdate;
  hrAddress.value = regDatas[this.className].address;
  sendToHidden.value = this.parentNode.className;
}



openPopup.addEventListener('click', hrRegistration);

function hrRegistration() {
  popupAreaModules[0].style.display = 'block'
}


for (i = 0; i < popupBgModules.length; i++) {
  popupBgModules[i].addEventListener("click", closedRegularlyDispatchBg)
}
SidemenuUseClose.addEventListener("click", closedRegularlyDispatchSideMenu)
popupCloseBtn[0].addEventListener("click", closedHrCrate)
popupCloseBtn[1].addEventListener("click", closedHrEdit)

function closedRegularlyDispatchBg() {
  for (i = 0; i < popupAreaModules.length; i++) {
    popupAreaModules[i].style.display = "none"
  }
}
function closedRegularlyDispatchSideMenu() {
  for (i = 0; i < popupAreaModules.length; i++) {
    popupAreaModules[i].style.display = "none"
  }
}
function closedHrCrate() {
  for (i = 0; i < popupAreaModules.length; i++) {
    popupAreaModules[i].style.display = "none"
  }
}
function closedHrEdit() {
  for (i = 0; i < popupAreaModules.length; i++) {
    popupAreaModules[i].style.display = "none"
  }
}


let checkCounte = false;

for (i = 0; i < checkBox.length; i++) {
  checkBox[i].addEventListener('change', checking)
}

function checking() {
  for (i = 0; i < checkBox.length; i++) {
    if (checkBox[i].checked) {
      checkCounte = true
    } else {
      checkCounte = false
    }
  }
}


hrMemberListForm.addEventListener('submit', deleteData)

function deleteData(e) {
  if (!checkCounte) {
    e.preventDefault()
    alert('삭제할 직원을 선택해 주세요.')
  }
}