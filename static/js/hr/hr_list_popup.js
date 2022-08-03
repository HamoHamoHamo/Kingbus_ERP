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
const btnModulesCreate = document.querySelector(".btnModulesCreate")
const PopupDataInputLicense = document.querySelector(".PopupDataInputLicense")
const hrRoleSelect = document.querySelector(".hrRole")



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
  hrID.value = regDatas[this.className].id
  sendToHidden.value = this.parentNode.className;
  if(hrRoleSelect.options[hrRoleSelect.selectedIndex].text ==  "운전원"){
    hrLicense.parentNode.style.visibility = "visible"
  }else{
    hrLicense.parentNode.style.visibility = "hidden"
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
btnModulesCreate.addEventListener('click', createChecker)
let selectedOption = ""
let idCheckCount = false

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


//원전원 이외에 면허번호 가림
PopupDataInputWork.addEventListener('change', showLicense)
hrRoleSelect.addEventListener('change', showLicenseEdit)

function showLicense(){
  if(PopupDataInputWork.options[PopupDataInputWork.selectedIndex].text ==  "운전원"){
    PopupDataInputLicense.parentNode.style.visibility = "visible"
  }else{
    PopupDataInputLicense.parentNode.style.visibility = "hidden"
  }
}
function showLicenseEdit(){
  if(hrRoleSelect.options[hrRoleSelect.selectedIndex].text ==  "운전원"){
    hrLicense.parentNode.style.visibility = "visible"
  }else{
    hrLicense.parentNode.style.visibility = "hidden"
  }
}