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
const createName = document.querySelector(".createName")
const createID = document.querySelector(".createID")
const hrID = document.querySelector(".hrID")



//직원상세
for (i = 0; i < editMember.length; i++) {
  editMember[i].addEventListener('click', openDetailPopup)
}

function openDetailPopup() {
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
  hrID.value = "리스트에서 아이디를 보여줄까 상세에서만 보여줄까?"
}



//직원등록
openPopup.addEventListener('click', hrRegistration);

function hrRegistration() {
  popupAreaModules[0].style.display = 'block'
  console.log(createName)
}

//이름 작성
if (createName.value == createID.value) {
  createName.addEventListener('change', nameChange)
}
function nameChange() {
  createID.value = createName.value
}



//팝업닫기
for (i = 0; i < popupBgModules.length; i++) {
  popupBgModules[i].addEventListener("click", closePopup)
  popupCloseBtn[i].addEventListener("click", closePopup)
}
SidemenuUseClose.addEventListener("click", closePopup)

function closePopup() {
  for (i = 0; i < popupAreaModules.length; i++) {
    popupAreaModules[i].style.display = "none"
  }
}


//삭제알림
let checkCounte = false;

for (i = 0; i < checkBox.length; i++) {
  checkBox[i].addEventListener('change', checking)
}

function checking() {
  checkCounte = false
  for (i = 0; i < checkBox.length; i++) {
    if (checkBox[i].checked) {
      checkCounte = true
    }
    console.log(checkBox[i].checked)
  }
}


hrMemberListForm.addEventListener('submit', deleteData)

function deleteData(e) {
  if (!checkCounte) {
    e.preventDefault()
    alert('삭제할 차량을 선택해 주세요.')
  } else {
    if (confirm('정말로 삭제하시겠습니까?') == false) {
      e.preventDefault()
    }
  }
}