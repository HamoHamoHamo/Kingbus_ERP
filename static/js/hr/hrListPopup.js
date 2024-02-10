const openPopup = document.querySelector('.addPeople');
const popupAreaModules = document.querySelectorAll('.popupAreaModules');
const popupBgModules = document.querySelectorAll(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const popupCloseBtn = document.querySelectorAll(".popupCloseBtn")
const checkBox = document.querySelectorAll(".tableBody td:nth-child(1) input")
const hrMemberListForm = document.querySelector(".hrMemberListForm")
const editMember = document.querySelectorAll(".tableBody td:nth-child(12)")
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
const popupEditId = document.querySelector(".popupEditId")
const popupRegisterId = document.querySelector(".popupRegisterId")
const hrEditPW = document.querySelector(".hrEditPW")
const hrRegisterPW = document.querySelector(".hrRegisterPW")
const memberForm = document.querySelector(".memberForm")
const btnModulesCreate = document.querySelectorAll(".btnModulesCreate")
const PopupDataInputLicense = document.querySelector(".PopupDataInputLicense")
const hrRoleSelect = document.querySelector(".hrRole")
const popupArticleBoxAllowanceType = document.querySelector(".popupArticleBoxAllowanceType")
const allowanceType = document.querySelector("#allowanceType")
const allowanceTypeOptions = document.querySelectorAll("#allowanceType option")

const popupTitle = document.querySelector(".popupHR")
const tableDocuments = document.querySelectorAll(".tableDocument")
const documentLabel = document.querySelectorAll("#documentPopup .popupArticleLabel")
const documentSendToHidden = document.querySelector(".documentSendToHidden")
const documentFiles = document.querySelectorAll(".documentFile")
const documentDeleteBtn = document.querySelectorAll(".documentDeleteBtn")

const essential = document.querySelectorAll(".essential")
const authorityDivision = document.querySelectorAll(".authorityDivision")

//const inputUse = document.querySelectorAll(".inputUse")

// 추가된 input 항목
const interview_date = document.querySelector("#interview_date")
const contract_date = document.querySelector("#contract_date")
const contract_renewal_date = document.querySelector("#contract_renewal_date")
const contract_condition = document.querySelector("#contract_condition")
const renewal_reason = document.querySelector("#renewal_reason")
const apply_path = document.querySelector("#apply_path")
const career = document.querySelector("#career")
const careerOptions = document.querySelectorAll("#career option")
const position_option = document.querySelectorAll("#position option")
const apprenticeship_note = document.querySelector("#apprenticeship_note")
const leave_reason = document.querySelector("#leave_reason")
const company = document.querySelector("#company")
const team = document.querySelector("#team")
const teamOptions = document.querySelectorAll("#team option")
const final_opinion = document.querySelector("#final_opinion")
const interviewer = document.querySelector("#interviewer")
const end_date = document.querySelector("#end_date")
const leave_date = document.querySelector("#leave_date")
const resident_number1 = document.querySelector("#resident_number1")
const resident_number2 = document.querySelector("#resident_number2")

let memberPopupStatus = ''

//직원상세
for (i = 0; i < editMember.length; i++) {
  editMember[i].addEventListener('click', openDetailPopup)
}

function openDetailPopup() {
  memberPopupStatus = 'edit'
  const data = regDatas[this.className];

  popupAreaModules[0].style.display = 'block'

  popupArticleBoxAllowanceType.style.display = 'none'
  allowanceType.setAttribute('name', '')
  
  popupTitle.innerText = "직원수정"
  memberForm.action = "/HR/member/edit"
  //비밀번호 부분 표시
  popupEditId.style.display = 'flex'
  popupRegisterId.style.display = 'none'
  hrEditPW.style.display = 'flex'
  hrRegisterPW.style.display = 'none'
  
  hrRole[0].selected = true;
  for (i = 0; i < hrRole.length; i++) {
    if (hrRole[i].innerText == data.role) {
      hrRole[i].selected = true;
      if (hrRole[i].innerText == '운전원') {
        popupArticleBoxAllowanceType.style.display = 'flex'
        allowanceType.setAttribute('name', 'allowance_type')
      }
    }
  }

  allowanceTypeOptions[0].selected = true;
  for (i = 0; i < allowanceTypeOptions.length; i++) {
    if (allowanceTypeOptions[i].innerText == data.allowance_type) {
      allowanceTypeOptions[i].selected = true;
    }
  }

  careerOptions[0].selected = true;
  for (i = 0; i < careerOptions.length; i++) {
    if (careerOptions[i].innerText == data.career) {
      careerOptions[i].selected = true;
    }
  }

  teamOptions[0].selected = true;
  for (i = 0; i < teamOptions.length; i++) {
    if (teamOptions[i].innerText == data.team) {
      teamOptions[i].selected = true;
    }
  }

  position_option[0].selected = true;
  for (i = 0; i < position_option.length; i++) {
    if (position_option[i].innerText == data.position) {
      position_option[i].selected = true;
    }
  }
  
  hrName.value = data.name;
  hrEntering.value = data.entering_date;
  hrPhone.value = data.phone_num;
  hrAddress.value = data.address;
  if(data.emergency !== ""){
    hrEmergency.value = data.emergency.split(" ")[0];
    hrReation.value = data.emergency.split(" ")[1];
  }else{
    hrEmergency.value = ""
    hrReation.value = ""
  }
  if(data.use === "사용"){
    hrUse[0].checked = true
  }else if (data.use === "미사용"){
    hrUse[1].checked = true
  }
  hrBlanck.value = data.note;
  
  //authorityDivision[2].style.display = "block"
  //authorityDivision[3].style.display = "flex"
  hrID.value = data.id
  
  sendToHidden.value = this.parentNode.className;
  
  interview_date.value = data.interview_date
  contract_date.value = data.contract_date
  contract_renewal_date.value = data.contract_renewal_date
  contract_condition.value = data.contract_condition
  renewal_reason.value = data.renewal_reason
  apply_path.value = data.apply_path
  apprenticeship_note.value = data.apprenticeship_note ? data.apprenticeship_note : '';
  leave_reason.value = data.leave_reason ? data.leave_reason : '';
  company.value = data.company

  final_opinion.value = data.final_opinion
  interviewer.value = data.interviewer
  end_date.value = data.end_date
  leave_date.value = data.leave_date
  resident_number1.value = data.resident_number1
  resident_number2.value = data.resident_number2
}



//직원등록
openPopup.addEventListener('click', hrRegistration);

function hrRegistration() {
  memberPopupStatus = 'create'
  popupAreaModules[0].style.display = 'block'

  popupArticleBoxAllowanceType.style.display = 'none'
  allowanceType.setAttribute('name', '')

  popupTitle.innerText = "직원등록"
  memberForm.action = "/HR/member/create"

  //id 비밀번호 부분 표시
  popupEditId.style.display = 'none'
  popupRegisterId.style.display = 'flex'
  hrEditPW.style.display = 'none'
  hrRegisterPW.style.display = 'block'

  hrRole[0].selected = true;
  careerOptions[0].selected = true;
  teamOptions[0].selected = true;
  position_option[0].selected = true;
  
  hrName.value = "";
  hrEntering.value = "";
  hrPhone.value = "";
  hrAddress.value = "";
  hrEmergency.value = "";
  hrReation.value = "";

  hrUse[0].checked = true

  hrBlanck.value = ""
  hrID.value = ""
  
  sendToHidden.value = ""
  
  interview_date.value = ""
  contract_date.value = ""
  contract_renewal_date.value = ""
  contract_condition.value = ""
  renewal_reason.value = ""
  apply_path.value = ""
  apprenticeship_note.value = ""
  leave_reason.value = ""
  company.value = ""

  final_opinion.value = ""
  interviewer.value = ""
  end_date.value = ""
  leave_date.value = ""
  resident_number1.value = ""
  resident_number2.value = ""
}

// 담당업무 운전원일 경우만 기사수당 기준 입력창 보이게 
hrRoleSelect.addEventListener('change', () => {
  if (hrRoleSelect.options[hrRoleSelect.selectedIndex].value == '운전원') {
    popupArticleBoxAllowanceType.style.display = 'flex'
    allowanceType.setAttribute('name', 'allowance_type')
  }
  else {
    popupArticleBoxAllowanceType.style.display = 'none'
    allowanceType.setAttribute('name', '')
  }
})


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
      console.log("TEST", i, essential[i])
      return alert("입력하지 않은 필수 입력사항이 있습니다.")
    }
  };
  if (PopupDataInputWork.options[PopupDataInputWork.selectedIndex].value == "") {
    return alert("입력하지 않은 필수 입력사항이 있습니다.")
  }
  if (memberPopupStatus == 'create' && PopupDataInputWork.options[PopupDataInputWork.selectedIndex].value !== "임시"){
    if (!idCheckCount) {
      return alert("아이디 중복확인을 진행해 주세요.")
    }
    if (createID.attributes.check_result.value == "fail") {
      return alert("이미 사용중인 아이디 입니다.")
    }
  }
  memberForm.submit()
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
    alert('삭제할 직원을 선택해 주세요.')
  } else {
    if (confirm('정말로 삭제하시겠습니까?') == false) {
      e.preventDefault()
    }
  }
}


//비밀번호 초기화 
hrEditPW.addEventListener('click', resetPW)

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


//구비서류 팝업
for (i = 0; i < tableDocuments.length; i++) {
  tableDocuments[i].addEventListener('click', openDocumentPopup)
}

function openDocumentPopup() {
  popupAreaModules[2].style.display = 'block'
  documentSendToHidden.value = this.parentNode.className;

  const datas = fileDatas[this.classList[1]];
  

  for (i = 0; i < documentLabel.length; i++) {
    let type = documentLabel[i].innerText;
    let label = documentLabel[i];
    
    // 초기화
    label.nextElementSibling.children[2].value = ''
    label.nextElementSibling.children[4].value = ''

    for (j = 0; j < datas.length; j++) {
      let data = datas[j];
      if (data['type'] == type) {
        // console.log("AAAAA",data)
        // console.log("AAAAA",label.nextElementSibling.children[4])
        label.nextElementSibling.children[2].value = data['filename']
        label.nextElementSibling.children[2].addEventListener("click", () => getDownloadUrl(data))
        label.nextElementSibling.children[4].value = data['id']
        break
      }
    }
  }
}

function getDownloadUrl(data) {
  window.open(`member/file/${data['id']}`, data['type'], "width=630, height=891")
}

//파일명 변경
for (i = 0; i < documentFiles.length; i++) {
  documentFiles[i].addEventListener('change', changeFileText)
}

function changeFileText() {
  console.log("TEST", this.nextElementSibling, this.files[0].name)
  this.nextElementSibling.value = this.files[0].name
  // console.log("tset", this.parentNode.children[4])
  // 삭제용 name값 초기화
  this.parentNode.children[4].name = ''
  
}

// 파일삭제
for (i = 0; i < documentDeleteBtn.length; i++) {
  documentDeleteBtn[i].addEventListener('click', deleteFile)
}

function deleteFile() {
  this.previousElementSibling.previousElementSibling.value = ""
  this.previousElementSibling.value = ""
  this.nextElementSibling.name = "delete_file_id"
  console.log(this.nextElementSibling)
}
