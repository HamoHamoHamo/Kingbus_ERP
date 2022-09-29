const openCrete = document.querySelector(".addVehicle")
const popupAreaModules = document.querySelectorAll(".popupAreaModules")
const popupBgModules = document.querySelectorAll(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const PopupCloseBtn = document.querySelectorAll(".closeBtn")
const openDetail = document.querySelectorAll(".tableBody td:nth-child(3)")
const editBtn = document.querySelector(".editBtn")
const saveBtn = document.querySelector(".saveBtn")
const PopupTitle = document.querySelectorAll(".popupTitle")
const popupSectionDetail = document.querySelector(".popupSectionDetail")
const PopupDataAreaEdit = document.querySelector(".popupSectionEdit")
const checkBox = document.querySelectorAll(".tableBody input")
const vehicleListForm = document.querySelector(".vehicleListForm")
const PopupData = document.querySelectorAll(".PopupData")
const vehicleNum1 = document.querySelector(".vehicleNum1")
const vehicleNum2 = document.querySelector(".vehicleNum2")
const driver_name = document.querySelectorAll(".driver_name option")
const use = document.querySelectorAll(".use option")
const maker = document.querySelector(".maker")
const vehicle_type = document.querySelector(".vehicle_type")
const vehicle_id = document.querySelector(".vehicle_id")
const model_year = document.querySelector(".model_year")
const release_date = document.querySelector(".release_date")
const passenger_num = document.querySelector(".passenger_num")
const motor_type = document.querySelector(".motor_type")
const rated_output = document.querySelector(".rated_output")
const insurance_expiry_date = document.querySelector(".insurance_expiry_date")
const check_duration = document.querySelector(".check_duration")
const sendToHidden = document.querySelector(".sendToHidden")
const fileDeleteBtn = document.querySelectorAll(".fileDeleteBtn")
const BusLicenseFileText = document.querySelector(".BusLicenseFileText")
const BusLicenseFileInput = document.querySelector(".BusLicenseFileInput")
const insuranceFileText = document.querySelector(".insuranceFileText")
const insuranceFileInput = document.querySelector(".insuranceFileInput")
const BusLicenseFileTextEdit = document.querySelector(".BusLicenseFileTextEdit")
const BusLicenseFileInputEdit = document.querySelector(".BusLicenseFileInputEdit")
const insuranceFileTextEdit = document.querySelector(".insuranceFileTextEdit")
const insuranceFileInputEdit = document.querySelector(".insuranceFileInputEdit")
const addUnit1 = document.querySelectorAll(".tableBody td:nth-child(6)")
const addUnit2 = document.querySelectorAll(".tableBody td:nth-child(7)")
const PopupDataInput = document.querySelectorAll(".PopupDataInput")
const createBtn = document.querySelectorAll(".createBtn")


//등록팝업 열기
openCrete.addEventListener("click", openCreatePopup)

function openCreatePopup() {
  popupAreaModules[0].style.display = "block"
}



//팝업닫기
for (i = 0; i < popupAreaModules.length; i++) {
  popupBgModules[i].addEventListener("click", closePopup)
  PopupCloseBtn[i].addEventListener("click", closePopup)
}
SidemenuUseClose.addEventListener("click", closePopup)

function closePopup() {
  for (i = 0; i < popupAreaModules.length; i++) {
    popupAreaModules[i].style.display = "none"
  }
  popupSectionDetail.style.display = "flex"
  PopupDataAreaEdit.style.display = "none"
  PopupTitle[1].innerText = "차량상세"
  editBtn.style.display = "flex";
  saveBtn.style.display = "none";
}



//상세팝업 열기
for (i = 0; i < openDetail.length; i++) {
  openDetail[i].addEventListener("click", openDetailPopup)
}

function openDetailPopup() {
  popupAreaModules[1].style.display = "block"
  PopupData[0].innerText = regDatas[this.className].vehicle_num0
  PopupData[1].innerText = regDatas[this.className].vehicle_num
  PopupData[2].innerText = regDatas[this.className].driver_name
  PopupData[3].innerText = regDatas[this.className].use
  PopupData[4].innerText = regDatas[this.className].maker
  PopupData[5].innerText = regDatas[this.className].vehicle_type
  PopupData[6].innerText = regDatas[this.className].vehicle_id
  PopupData[8].innerText = regDatas[this.className].model_year
  PopupData[9].innerText = regDatas[this.className].release_date
  PopupData[10].innerText = regDatas[this.className].passenger_num
  PopupData[11].innerText = regDatas[this.className].motor_type
  PopupData[12].innerText = regDatas[this.className].rated_output
  PopupData[14].innerText = regDatas[this.className].check_duration
  PopupData[15].innerText = regDatas[this.className].vehicle_registration
  PopupData[16].innerText = regDatas[this.className].insurance_receipt
  vehicleNum1.value = regDatas[this.className].vehicle_num0
  vehicleNum2.value = regDatas[this.className].vehicle_num
  for (i = 0; i < driver_name.length; i++) {
    if (driver_name[i].innerText == regDatas[this.className].driver_name) {
      driver_name[i].selected = true;
    }
  }
  for (i = 0; i < use.length; i++) {
    if (use[i].innerText == regDatas[this.className].use) {
      use[i].selected = true;
    }
  }
  maker.value = regDatas[this.className].maker
  vehicle_type.value = regDatas[this.className].vehicle_type
  vehicle_id.value = regDatas[this.className].vehicle_id
  model_year.value = regDatas[this.className].model_year
  release_date.value = regDatas[this.className].release_date
  passenger_num.value = regDatas[this.className].passenger_num
  motor_type.value = regDatas[this.className].motor_type
  rated_output.value = regDatas[this.className].rated_output
  check_duration.value = regDatas[this.className].check_duration
  BusLicenseFileTextEdit.value = regDatas[this.className].vehicle_registration
  insuranceFileTextEdit.value = regDatas[this.className].insurance_receipt
  sendToHidden.value = this.parentNode.className;
}


//상세->수정
editBtn.addEventListener("click", changeEdit)

function changeEdit() {
  popupSectionDetail.style.display = "none"
  PopupDataAreaEdit.style.display = "block"
  PopupTitle[1].innerText = "차량수정"
  editBtn.style.display = "none";
  createBtn[1].style.display = "flex";
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


vehicleListForm.addEventListener('submit', deleteData)

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


//파일명 변경
BusLicenseFileInput.addEventListener("change", changeFileBusLicense)
insuranceFileInput.addEventListener("change", changeFileinsurance)
BusLicenseFileInputEdit.addEventListener("change", changeFileLicenseEdit)
insuranceFileInputEdit.addEventListener("change", changeFileDriverLicenseEdit)

function changeFileBusLicense() {
  BusLicenseFileText.value = BusLicenseFileInput.files[0].name
}
function changeFileinsurance() {
  insuranceFileText.value = insuranceFileInput.files[0].name
}
function changeFileLicenseEdit() {
  BusLicenseFileTextEdit.value = BusLicenseFileInputEdit.files[0].name
}
function changeFileDriverLicenseEdit() {
  insuranceFileTextEdit.value = insuranceFileInputEdit.files[0].name
}




// 파일삭제
fileDeleteBtn[0].addEventListener("click", deleteFileBusLicense)
fileDeleteBtn[1].addEventListener("click", deleteFileInsurance)
fileDeleteBtn[2].addEventListener("click", deleteFileLicensEdit)
fileDeleteBtn[3].addEventListener("click", deleteFileDriverLicensEdit)

function deleteFileBusLicense() {
  BusLicenseFileText.value = ""
  BusLicenseFileInput.value = ""
}
function deleteFileInsurance() {
  insuranceFileText.value = ""
  insuranceFileInput.value = ""
}
function deleteFileLicensEdit() {
  BusLicenseFileTextEdit.value = ""
  BusLicenseFileInputEdit.value = ""
}
function deleteFileDriverLicensEdit() {
  insuranceFileTextEdit.value = ""
  insuranceFileInputEdit.value = ""
}




// , 추가, 단위추가
window.onload = function () {
  for (i = 0; i < addUnit1.length; i++) {
      if (addUnit1[i].innerText !== "") {
          addUnit1[i].innerText = `${addUnit1[i].innerText}명`
      }
      if (addUnit2[i].innerText !== "") {
          addUnit2[i].innerText = `${addUnit2[i].innerText}년`
      }
  }
}

//차량번호, 연식
// PopupDataInput[1].addEventListener('change', busNumChecker)
// PopupDataInput[7].addEventListener('change', yearChecker)

// function busNumChecker(){
//   if(this.value.length >= 5){
//     this.value = this.value.substr(0,5)
//   }else if(this.value.length <= 3){
//     alert("4자리의 숫자를 입력해 주세요.")
//   }
// }
// function yearChecker(){
//   if(this.value.length >= 5){
//     this.value = this.value.substr(0,4)
//   }else if(this.value.length <= 3){
//     alert("4자리의 숫자를 입력해 주세요.")
//   }
  // else if(this.value.substr(2,) !== 19 && this.value.substr(2,) !== 20){
  //   alert("올바른 연도를 입력해 주세요")
  //   this.value = ""
  // }
// }