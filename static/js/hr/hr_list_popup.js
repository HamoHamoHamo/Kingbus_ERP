const openPopup = document.querySelector('.member-create');
const popupAreaModules = document.querySelectorAll('.popupAreaModules');
const popupBgModules = document.querySelectorAll(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const popupCloseBtn = document.querySelectorAll(".popupCloseBtn")
const deleteForm = document.querySelector(".member-delete-form")
const editMember = document.querySelectorAll(".table-list_body-tr_td:nth-child(9)")
const hrName = document.querySelector(".hrName")
const hrRole = document.querySelectorAll(".hrRole option")
const hrEntering = document.querySelector(".hrEntering")
const hrPhone = document.querySelector(".hrPhone")
const hrBirth = document.querySelector(".hrBirth")
const hrAddress = document.querySelector(".hrAddress")
const hrEmergency = document.querySelector(".hrEmergency")
const sendToHidden = document.querySelector(".sendToHidden")
const createName = document.querySelector(".createName")
const PopupDataInputWork = document.querySelector(".PopupDataInputWork")
const selectOption = document.querySelectorAll(".PopupDataInputWork option")
const PopupDataInputEntering = document.querySelector(".PopupDataInputEntering")
const PopupDataInputPhoneNum = document.querySelector(".PopupDataInputPhoneNum")
const PopupDataInputBirth = document.querySelector(".PopupDataInputBirth")
const PopupDataInputAddress = document.querySelector(".PopupDataInputAddress")
const PopupDataInputBlack = document.querySelector(".PopupDataInputBlack")
const createID = document.querySelector(".createID")
const hrID = document.querySelector(".hrID")
const hrPW = document.querySelector(".hrPW")
const editPopupContainer = document.querySelector(".editPopupContainer")
const btnModulesCreate = document.querySelector(".btnModulesCreate")
const PopupDataInputLicense = document.querySelector(".PopupDataInputLicense")
const hrRoleSelect = document.querySelector(".hrRole")
const fileDeleteBtn = document.querySelectorAll(".fileDeleteBtn")
const FileTextLicense = document.querySelector(".LicenseFileText")
const FileInputLicense = document.querySelector(".LicenseFileInput")
const hrBlank = document.querySelector(".hrBlank")
const FileTextDriverLicense = document.querySelector(".DriverLicenseFileText")
const FileInputDriverLicense = document.querySelector(".DriverLicenseFileInput")

const LicenseFileTextEdit = document.querySelector(".LicenseFileTextEdit")
const LicenseFileInputEdit = document.querySelector(".LicenseFileInputEdit")

const DriverLicenseFileTextEdit = document.querySelector(".DriverLicenseFileTextEdit")
const DriverLicenseFileInputEdit = document.querySelector(".DriverLicenseFileInputEdit")

const tableArea = document.querySelector(".table-list-area")


//직원상세
for (i = 0; i < editMember.length; i++) {
  editMember[i].addEventListener('click', openDetailPopup)
}

function openDetailPopup(targetId) {
  for (i = 0; i < regDatas.length; i++){
    if(regDatas[i].user_id == targetId){
      popupAreaModules[1].style.display = 'block'
      hrName.value = regDatas[i].name;
      for (j = 0; j < hrRole.length; j++) {
        if (hrRole[j].innerText == regDatas[i].role) {
          hrRole[j].selected = true;
        }
      }
      hrEntering.value = regDatas[i].entering_date;
      hrPhone.value = regDatas[i].phone_num;
      hrBirth.value = regDatas[i].birthdate;
      hrAddress.value = regDatas[i].address;
      // hrEmergency.value = regDatas[i].hrEmergency;
      hrID.value = regDatas[i].id
      LicenseFileTextEdit.value = regDatas[i].license
      DriverLicenseFileTextEdit.value = regDatas[i].bus_license
      hrBlank.value = regDatas[i].note
    }
  };
  sendToHidden.value = targetId;
}



//직원등록
openPopup.addEventListener('click', hrRegistration);

function hrRegistration() {
  popupAreaModules[0].style.display = 'block'
}


//이름 작성
if (createName.value == createID.value) {
  createName.addEventListener('input', nameChange)
}
function nameChange() {
  createID.value = createName.value
  idCheckCount = false
}


//직원등록 조건검사
btnModulesCreate.addEventListener('click', createChecker)
let selectedOption = ""
let idCheckCount = false
let date = new Date();
let year = date.getFullYear();
let month = ("0" + (1 + date.getMonth())).slice(-2);
let day = ("0" + date.getDate()).slice(-2);
let onlyNumber = /[^0-9]/g;
let birthPAttern = /^(19[0-9][0-9]|20\d{2})(0[0-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])$/

function createChecker(e) {
  for (i = 0; i < selectOption.length; i++) {
    if (selectOption[i].selected) {
      selectedOption = selectOption[i]
    }
  }
  if (createName.value == "" || selectedOption.value == "" || PopupDataInputEntering.value == "" || PopupDataInputPhoneNum.value == "" || PopupDataInputBirth.value == "" || PopupDataInputAddress.value == "" || createID.value == "") {
    alert("입력하지 않은 항목이 있습니다.")
    e.preventDefault()
  } else if (!idCheckCount) {
    alert("아이디 중복확인을 진행해 주세요.")
    e.preventDefault()
  } else if (createID.attributes.check_result.value == "fail") {
    alert("이미 사용중인 아이디 입니다.")
    e.preventDefault()
  }
}

//전화번호
PopupDataInputPhoneNum.addEventListener('change', phoneNumChecker)
hrPhone.addEventListener('change', phoneNumChecker)

function phoneNumChecker() {
  this.value.replace(onlyNumber, "")
  if (this.value.length <= 8 || this.value.length >= 12) {
    alert("형식에 맞지않는 전화번호 입니다.")
    this.value = ""
  }
  this.value = this.value.replace(/\-/g, "")
  this.value = this.value.replace(/^(\d{2,3})(\d{3,4})(\d{4})$/, `$1-$2-$3`)
}

//생년월일
PopupDataInputBirth.addEventListener('change', birthChecker)

function birthChecker() {
  if (!birthPAttern.test(this.value)) {
    alert("형식에 맞지 않습니다.")
    this.value = ""
  }
}


//팝업닫기
for (i = 0; i < popupBgModules.length; i++) {
  popupBgModules[i].addEventListener("click", closePopup)
  popupCloseBtn[i].addEventListener("click", closePopup)
}
SidemenuUseClose.addEventListener("click", closePopup)

function closePopup() {
  idCheckCount = false
  createID.removeAttribute("check_result")
  for (i = 0; i < popupAreaModules.length; i++) {
    popupAreaModules[i].style.display = "none"
  }
  createName.value = ""
  PopupDataInputWork.children[0].selected = true
  PopupDataInputEntering.value = ""
  PopupDataInputPhoneNum.value = ""
  PopupDataInputBirth.value = ""
  PopupDataInputAddress.value = ""
  PopupDataInputBlack.value = ""
  createID.value = ""
  FileTextLicense.value = ""
  if (FileTextLicense.value !== "") {
    FileInputLicense.files[0].name = ""
  }
  FileTextDriverLicense.value = ""
  if (FileTextDriverLicense.value !== "") {
    FileInputDriverLicense.files[0].name = ""
  }
  uploadFileText.value = ""
  uploadFile.value = ""
  uploadLicenseFileText.value = ""
  uploadLicenseFile.value = ""
  uploadDriverLicenseFileText.value = ""
  uploadDriverLicenseFile.value = ""
}

// checkbox 생성
tableArea.addEventListener("mouseover", createCheckbox)

let checkCounte = false;

function createCheckbox() {
  const checkBox = document.querySelectorAll(".table-list_body-tr_td:nth-child(1) input")

  //삭제알림

  for (i = 0; i < checkBox.length; i++) {
    checkBox[i].addEventListener('change', checking)
  }

  function checking() {
    for (i = 0; i < checkBox.length; i++) {
      if (checkBox[i].checked) {
        return checkCounte = true
      }
    }
  }
}




deleteForm.addEventListener('submit', deleteData)

function deleteData(e) {
  if (!checkCounte) {
    e.preventDefault()
    alert('삭제할 차량을 선택해 주세요.')
  } else {
    if (confirm('정말로 삭제하시겠습니까?')) {
      e.preventDefault()
      deleteForm.submit()
    }
  }
}


//비밀번호 초기화 
hrPW.addEventListener('click', resetPW)

async function resetPW() {
  await fetch(url = `/member/reset/password?id=${sendToHidden.value}`, {
  });
  return alert("비밀번호가 초기화 되었습니다.")
}


// 아이디 중복검사
function id_overlap_check_hr() {
  idCheckCount = true

  $('.createID').change(function () {
    $('.createID').attr("check_result", "fail");
  })


  if ($('.createID').val() == '') {
    alert('아이디를 입력해주세요.')
    return;
  }

  $.ajax({
    url: "/member/id-check",
    data: {
      'user_id': createID.value
    },
    datatype: 'json',
    success: function (data) {
      console.log(data['overlap']);
      if (data['overlap'] == "fail") {
        alert("이미 존재하는 아이디 입니다.");
        createID.focus();
        return;
      } else {
        alert("사용가능한 아이디 입니다.");
        $('.createID').attr("check_result", "success");
        return;
      }
    },
    error: function (request, status, error) {
      console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
      // ajax 처리가 결과가 에러이면 전송 여부는 false // 앞서 초기값을 false로 해 놓았지만 한번 더 선언을 한다.
    }
  });
}





//파일명 변경
FileInputLicense.addEventListener("change", changeFileLicense)
FileInputDriverLicense.addEventListener("change", changeFileDriverLicense)
LicenseFileInputEdit.addEventListener("change", changeFileLicenseEdit)
DriverLicenseFileInputEdit.addEventListener("change", changeFileDriverLicenseEdit)

function changeFileLicense() {
  FileTextLicense.value = FileInputLicense.files[0].name
}
function changeFileDriverLicense() {
  FileTextDriverLicense.value = FileInputDriverLicense.files[0].name
}
function changeFileLicenseEdit() {
  LicenseFileTextEdit.value = LicenseFileInputEdit.files[0].name
}
function changeFileDriverLicenseEdit() {
  DriverLicenseFileTextEdit.value = DriverLicenseFileInputEdit.files[0].name
}




// 파일삭제
fileDeleteBtn[0].addEventListener("click", deleteFileLicens)
fileDeleteBtn[1].addEventListener("click", deleteFileDriverLicens)
fileDeleteBtn[2].addEventListener("click", deleteFileLicensEdit)
fileDeleteBtn[3].addEventListener("click", deleteFileDriverLicensEdit)

function deleteFileLicens() {
  FileTextLicense.value = ""
  FileInputLicense.value = ""
}
function deleteFileDriverLicens() {
  FileTextDriverLicense.value = ""
  FileInputDriverLicense.value = ""
}
function deleteFileLicensEdit() {
  LicenseFileTextEdit.value = ""
  LicenseFileInputEdit.value = ""
}
function deleteFileDriverLicensEdit() {
  DriverLicenseFileTextEdit.value = ""
  DriverLicenseFileInputEdit.value = ""
}