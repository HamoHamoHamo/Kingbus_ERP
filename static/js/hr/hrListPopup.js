const openPopup = document.querySelector('.addPeople');
const popupAreaModules = document.querySelectorAll('.popupAreaModules');
const popupBgModules = document.querySelectorAll(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const popupCloseBtn = document.querySelectorAll(".popupCloseBtn")
const checkBox = document.querySelectorAll(".tableBody td:nth-child(1) input")
const hrMemberListForm = document.querySelector(".hrMemberListForm")
const editMember = document.querySelectorAll(".tableBody td:nth-child(3)")
const phoneNum = document.querySelectorAll(".tableBody td:nth-child(8)")
const birthday = document.querySelectorAll(".tableBody td:nth-child(9)")
const hrName = document.querySelector(".hrName")
const hrRole = document.querySelectorAll(".hrRole option")
const hrEntering = document.querySelector(".hrEntering")
const hrPhone = document.querySelector(".hrPhone")
const hrBirth = document.querySelector(".hrBirth")
const hrAddress = document.querySelector(".hrAddress")
const hrEmergency = document.querySelector(".hrEmergency")
const hrReation = document.querySelector(".hrReation")
const hrBlanck = document.querySelector(".hrBlanck")
const hrUse = document.querySelectorAll(".hrUse")
const sendToHidden = document.querySelector(".sendToHidden")
const createName = document.querySelector(".createName")
const PopupDataInputWork = document.querySelector(".PopupDataInputWork")
const selectOption = document.querySelectorAll(".PopupDataInputWork option")
const PopupDataInputEntering = document.querySelector(".PopupDataInputEntering")
const PopupDataInputPhoneNum = document.querySelector(".PopupDataInputPhoneNum")
const PopupDataInputBirth = document.querySelector(".PopupDataInputBirth")
const PopupDataInputAddress = document.querySelector(".PopupDataInputAddress")
const createID = document.querySelector(".createID")
const hrID = document.querySelector(".hrID")
const hrPW = document.querySelector(".hrPW")
const editPopupContainer = document.querySelector(".editPopupContainer")
const btnModulesCreate = document.querySelectorAll(".btnModulesCreate")
const PopupDataInputLicense = document.querySelector(".PopupDataInputLicense")
const hrRoleSelect = document.querySelector(".hrRole")
const fileDeleteBtn = document.querySelectorAll(".fileDeleteBtn")
const FileTextLicense = document.querySelector(".LicenseFileText")
const FileInputLicense = document.querySelector(".LicenseFileInput")
const FileTextDriverLicense = document.querySelector(".DriverLicenseFileText")
const FileInputDriverLicense = document.querySelector(".DriverLicenseFileInput")

const LicenseFileTextEdit = document.querySelector(".LicenseFileTextEdit")
const LicenseFileInputEdit = document.querySelector(".LicenseFileInputEdit")

const DriverLicenseFileTextEdit = document.querySelector(".DriverLicenseFileTextEdit")
const DriverLicenseFileInputEdit = document.querySelector(".DriverLicenseFileInputEdit")

const memberFormCreate = document.querySelector(".memberFormCreate")
const essential = document.querySelectorAll(".essential")
const authorityDivision = document.querySelectorAll(".authorityDivision")

// 추가된 input 항목 8개
const interview_date = document.querySelector("#interview_date")
const contract_date = document.querySelector("#contract_date")
const contract_renewal_date = document.querySelector("#contract_renewal_date")
const contract_condition = document.querySelector("#contract_condition")
const renewal_reason = document.querySelector("#renewal_reason")
const apply_path = document.querySelector("#apply_path")
const career = document.querySelector("#career")
const position_option = document.querySelectorAll("#position option")


//직원상세
for (i = 0; i < editMember.length; i++) {
  editMember[i].addEventListener('click', openDetailPopup)
}

function openDetailPopup() {
  popupAreaModules[1].style.display = 'block'
  
  for (i = 0; i < hrRole.length; i++) {
    if (hrRole[i].innerText == regDatas[this.className].role) {
      hrRole[i].selected = true;
    }
  }
  
  hrName.value = regDatas[this.className].name;
  hrEntering.value = regDatas[this.className].entering_date;
  hrPhone.value = regDatas[this.className].phone_num;
  hrBirth.value = regDatas[this.className].birthdate;
  hrAddress.value = regDatas[this.className].address;
  if(regDatas[this.className].emergency !== ""){
    hrEmergency.value = regDatas[this.className].emergency.split(" ")[0];
    hrReation.value = regDatas[this.className].emergency.split(" ")[1];
  }else{
    hrEmergency.value = ""
    hrReation.value = ""
  }
  if(regDatas[this.className].use === "사용"){
    hrUse[0].checked = true
  }else if (regDatas[this.className].use === "미사용"){
    hrUse[1].checked = true
  }
  hrBlanck.value = regDatas[this.className].note;
  
  authorityDivision[2].style.display = "block"
  authorityDivision[3].style.display = "flex"
  hrID.value = regDatas[this.className].id
  
  LicenseFileTextEdit.value = regDatas[this.className].license
  DriverLicenseFileTextEdit.value = regDatas[this.className].bus_license
  sendToHidden.value = this.parentNode.className;
  
  interview_date.value = regDatas[this.className].interview_date
  contract_date.value = regDatas[this.className].contract_date
  contract_renewal_date.value = regDatas[this.className].contract_renewal_date
  contract_condition.value = regDatas[this.className].contract_condition
  renewal_reason.value = regDatas[this.className].renewal_reason
  apply_path.value = regDatas[this.className].apply_path
  career.value = regDatas[this.className].career

  for (i = 0; i < position_option.length; i++) {
    if (position_option[i].innerText == regDatas[this.className].position) {
      position_option[i].selected = true;
    }
  }
}



//직원등록
openPopup.addEventListener('click', hrRegistration);

function hrRegistration() {
  popupAreaModules[0].style.display = 'block'
}


//이름 작성
if (createName.value == createID.value) {
  createName.addEventListener('change', nameChange)
}
function nameChange() {
  createID.value = createName.value
  idCheckCount = false
}


//직원등록 조건검사
btnModulesCreate[0].addEventListener('click', createChecker)
let selectedOption = ""
let idCheckCount = false
let date = new Date();
let year = date.getFullYear();
let month = ("0" + (1 + date.getMonth())).slice(-2);
let day = ("0" + date.getDate()).slice(-2);
let onlyNumber = /[^0-9]/g;
let birthPAttern = /^(19[0-9][0-9]|20\d{2})(0[0-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])$/

function createChecker() {
  for (i = 0; i < essential.length; i++) {
    if (essential[i].value == "") {
      return alert("입력하지 않은 필수 입력사항이 있습니다.")
    }
  };
  if (PopupDataInputWork.options[PopupDataInputWork.selectedIndex].value == "") {
    return alert("입력하지 않은 필수 입력사항이 있습니다.")
  }
  if(PopupDataInputWork.options[PopupDataInputWork.selectedIndex].value !== "임시"){
    if (!idCheckCount) {
      alert("아이디 중복확인을 진행해 주세요.")
      e.preventDefault()
    }
    if (createID.attributes.check_result.value == "fail") {
      alert("이미 사용중인 아이디 입니다.")
      e.preventDefault()
    }
  }
  memberFormCreate.submit()
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


//비밀번호 초기화 
hrPW.addEventListener('click', resetPW)

async function resetPW() {
  if (confirm('비밀번호를 0000으로 초기화 하시겠습니까?')){
    await fetch(url = `/member/reset/password?id=${sendToHidden.value}`, {
    });
    return alert("비밀번호가 초기화 되었습니다.")
  }
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


window.onload = function () {
  for (i = 0; i < phoneNum.length; i++) {
    phoneNum[i].innerText = phoneNum[i].innerText.replace(/^(\d{2,3})(\d{3,4})(\d{4})$/, `$1-$2-$3`)
    birthday[i].innerText = birthday[i].innerText.replace(/^(\d{4})(\d{2})(\d{2})$/, `$1-$2-$3`)
  }
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
  console.log('a');
  
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