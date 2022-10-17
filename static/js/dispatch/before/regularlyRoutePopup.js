const routeDetail = document.querySelectorAll(".tableBody td:nth-child(4)")
const popupAreaModulesRoute = document.querySelector(".popupAreaModulesRoute")
const popupBgModulesRoute = document.querySelectorAll(".popupBgModulesRoute")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const routePopupTitle = document.querySelector(".routePopupTitle")
const routePopupCloseBtn = document.querySelector(".routePopupBtnBox .btnModules:nth-child(1)")
const routePopupEditBtn = document.querySelector(".routePopupBtnBox .btnModules:nth-child(2)")
const routePopupSaveBtn = document.querySelector(".routePopupBtnBox input")
const routePoppupDetail = document.querySelector(".popupContainerRoute .routePopupDataArea:nth-child(3)")
const routePoppupEdit = document.querySelector(".popupContainerRoute .routePopupDataArea:nth-child(4)")
const routePopupDataDriveDateEdit = document.querySelectorAll(".popupAreaModulesRoute .routePopupDataDriveDate input")
const routePopupDataDriveDateEditLabel = document.querySelectorAll(".popupAreaModulesRoute .routePopupDataDriveDate label")
const routePopupDataDriveDateCreate = document.querySelectorAll(".popupAreaModulesRouteCreate .routePopupDataDriveDate input")
const groupMenagementBtn = document.querySelector(".gruopManagementBtn")
const routeCreateBtn = document.querySelector(".createRouteBtn")
const groupMenagementCloseBtn = document.querySelector(".groupMenagementCloseBtn")
const groupMenagementCreateBtn = document.querySelector(".groupMenagementCreateBtn")
const groupCretetCloseBtn = document.querySelector(".groupCretetCloseBtn")
const popupAreaModulesRouteCreate = document.querySelector(".popupAreaModulesRouteCreate")
const popupAreaModulesGroupCreate = document.querySelector(".popupAreaModulesGroupCreate")
const groupBox = document.querySelectorAll(".groupBox")
const groupBoxImg = document.querySelectorAll(".groupBox img")
const groupDepth2 = document.querySelectorAll(".groupDepth2")
const routePopupData = document.querySelectorAll(".routePopupData")
const routePopupDataGroupOption = document.querySelectorAll(".routePopupDataGroup option")
const routePopupDataDriveTime = document.querySelectorAll(".routePopupDataDriveTime input")
const routePopupDataRoutName = document.querySelectorAll(".routePopupDataRoutName")
const routePopupDataDriverNumber = document.querySelector(".routePopupDataDriverNumber")
const routePopupDataDriverPay = document.querySelectorAll(".routePopupDataDriverPay")
const routePopupDataBusKindsOption = document.querySelectorAll(".routePopupDataBusKinds option")
const routePopupDataBusCount = document.querySelector(".routePopupDataBusCount")
const routePopupDataContractPeriod = document.querySelectorAll(".routePopupDataContractPeriod input")
const routePopupDatAaccount = document.querySelector(".routePopupDatAaccount")
const routePopupPhoneNumber = document.querySelectorAll(".routePopupPhoneNumber")
const routePopupDataContractAmount = document.querySelectorAll(".routePopupDataContractAmount")
const routePopupWorkinput= document.querySelectorAll(".routePopupWork input")
const routePopupWorkLabel = document.querySelector(".routePopupWork label:nth-child(2)")
const routePopupDataReference = document.querySelector(".routePopupDataReference")
const sendToHidden = document.querySelector(".sendToHidden")
const editIcon = document.querySelectorAll(".groupBoxTollCell div")
const deletIcon = document.querySelectorAll(".groupBoxTollCell input")
const createGroupDataArea = document.querySelector(".createGroupDataArea")
const groupBoxTitle = document.querySelectorAll(".groupBoxTitle")
const groupBoxTitleHidden = document.querySelectorAll(".groupBoxTitleHidden")
const groupCheck = document.querySelectorAll(".tableBody td:nth-child(1) input")
const groupListForm = document.querySelector(".groupListForm")
const btnModulesGroupSave = document.querySelector(".btnModulesGroupSave")
const editOrDelete = document.querySelector(".editOrDelete")


let editOpenCount = true
let groupDelet = false
let groupSave = false


/*노선상세 */
for (i = 0; i < routeDetail.length; i++) {
  routeDetail[i].addEventListener("click", detailPopup)
}
function detailPopup() {
  popupAreaModulesRoute.style.display = "block"
  routePopupData[0].innerText = regDatas[this.className].group
  routePopupData[1].innerText = regDatas[this.className].departure
  routePopupData[2].innerText = `${regDatas[this.className].departure_time}~${regDatas[this.className].arrival_time}`
  routePopupData[3].innerText = regDatas[this.className].arrival
  routePopupData[4].innerText = regDatas[this.className].number
  routePopupData[5].innerText = regDatas[this.className].week
  routePopupData[6].innerText = `${regDatas[this.className].driver_allowance.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`;
  routePopupData[7].innerText = regDatas[this.className].bus_type
  routePopupData[8].innerText = `${regDatas[this.className].bus_cnt}대`
  routePopupData[9].innerText = regDatas[this.className].customer
  routePopupData[10].innerText = regDatas[this.className].customer_phone
  routePopupData[11].innerText = `${regDatas[this.className].price.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`;
  routePopupData[12].innerText = `${regDatas[this.className].contract_start_date}~${regDatas[this.className].contract_end_date}`
  routePopupData[13].innerText = regDatas[this.className].work_type
  routePopupData[14].innerText = regDatas[this.className].references
  for (i = 0; i < routePopupDataGroupOption.length; i++) {
    if (routePopupDataGroupOption[i].innerText == regDatas[this.className].group) {
      routePopupDataGroupOption[i].selected = true;
    }
  }
  routePopupDataDriveTime[0].value = regDatas[this.className].departure_time;
  routePopupDataDriveTime[1].value = regDatas[this.className].arrival_time;
  routePopupDataRoutName[0].value = regDatas[this.className].departure;
  routePopupDataRoutName[1].value = regDatas[this.className].arrival;
  routePopupDataDriverNumber.value = regDatas[this.className].number;
  routePopupDataDriverPay[0].value = regDatas[this.className].driver_allowance.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  for (i = 0; i < routePopupDataBusKindsOption.length; i++) {
    if (routePopupDataBusKindsOption[i].innerText == regDatas[this.className].bus_type) {
      routePopupDataBusKindsOption[i].selected = true;
    }
  }
  routePopupDataBusCount.value = regDatas[this.className].bus_cnt;
  routePopupDatAaccount.value = regDatas[this.className].customer;
  routePopupPhoneNumber[0].value = regDatas[this.className].customer_phone;
  routePopupDataContractAmount[0].value = regDatas[this.className].price.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  routePopupDataContractPeriod[0].value = regDatas[this.className].contract_start_date;
  routePopupDataContractPeriod[1].value = regDatas[this.className].contract_end_date;
  if (routePopupWorkLabel.innerText == regDatas[this.className].work_type) {
    routePopupWorkInput[0].checked = true;
  } else {
    routePopupWorkInput[1].checked = true;
  }
  routePopupDataReference.value = regDatas[this.className].references;
  let weekArray = regDatas[this.className].week.split('')
  let newWeekArray = weekArray.filter(item => item !== ' ')
  let weekAllCount = 0;
  for (i = 0; i < 8; i++) {
    routePopupDataDriveDateEdit[i].checked = false;
  }
  for (i = 1; i < routePopupDataDriveDateEdit.length; i++) {
    if (newWeekArray.find(item => item == routePopupDataDriveDateEditLabel[i].innerText)) {
      routePopupDataDriveDateEdit[i].checked = true;
      weekAllCount = weekAllCount + 1;
      if (weekAllCount == 7) {
        routePopupDataDriveDateEdit[0].checked = true;
      }
    }
  }
  sendToHidden.value = this.parentElement.className;
}

for (i = 0; i < 3; i++) {
  popupBgModulesRoute[i].addEventListener("click", closedRoutePopup)
}
SidemenuUseClose.addEventListener("click", closedRoutePopupMenu)
routePopupCloseBtn.addEventListener("click", closedRoutePopupBtn)
routePopupEditBtn.addEventListener("click", changeEdit)

function closedRoutePopup() {
  popupAreaModulesRoute.style.display = "none"
  popupAreaModulesRouteCreate.style.display = "none"
  popupAreaModulesGroupCreate.style.display = "none"
}
function closedRoutePopupMenu() {
  popupAreaModulesRoute.style.display = "none"
  popupAreaModulesRouteCreate.style.display = "none"
  popupAreaModulesGroupCreate.style.display = "none"
}
function closedRoutePopupBtn() {
  popupAreaModulesRoute.style.display = "none"
  routePopupTitle.innerText = "노선상세"
  routePopupEditBtn.style.display = "flex"
  routePopupSaveBtn.style.display = "none"
  routePoppupDetail.style.display = "flex"
  routePoppupEdit.style.display = "none"
}
function changeEdit() {
  routePopupTitle.innerText = "노선수정"
  routePopupEditBtn.style.display = "none"
  routePopupSaveBtn.style.display = "flex"
  routePoppupDetail.style.display = "none"
  routePoppupEdit.style.display = "flex"
}




/*노선상세 모두체크*/
routePopupDataDriveDateEdit[0].addEventListener('change', allcheckedEdit)

function allcheckedEdit() {
  if (routePopupDataDriveDateEdit[0].checked) {
    for (i = 1; i < 8; i++) {
      routePopupDataDriveDateEdit[i].checked = true;
    }

  } else {
    for (i = 1; i < 8; i++) {
      routePopupDataDriveDateEdit[i].checked = false;
    }
  }
}

for (i = 1; i < 8; i++) {
  routePopupDataDriveDateEdit[i].addEventListener('change', changeAllCheckEdit)
}

function changeAllCheckEdit() {
  if (routePopupDataDriveDateEdit[1].checked && routePopupDataDriveDateEdit[2].checked && routePopupDataDriveDateEdit[3].checked && routePopupDataDriveDateEdit[4].checked && routePopupDataDriveDateEdit[5].checked && routePopupDataDriveDateEdit[6].checked && routePopupDataDriveDateEdit[7].checked) {
    routePopupDataDriveDateEdit[0].checked = true;
  } else {
    routePopupDataDriveDateEdit[0].checked = false;
  }
}





/*그룹관리*/
groupMenagementBtn.addEventListener('click', openGroupMenagement)
groupCretetCloseBtn.addEventListener('click', closeGroupMenagement)

function openGroupMenagement() {
  editOpenCount = true
  popupAreaModulesGroupCreate.style.display = "flex"
  for (i = 0; i < groupBoxTitle.length; i++) {
    groupBoxTitle[i].value = `${groupList[i]}`
  }
}

function closeGroupMenagement() {
  popupAreaModulesGroupCreate.style.display = "none"
  for (i = 0; i < groupBoxTitle.length; i++) {
    groupBoxTitle[i].style.border = 0;
    groupBoxTitle[i].style.cursor = "pointer";
    groupBoxTitle[i].style.outline = "none";
    groupBoxTitle[i].readOnly = true
  }
  for (i = 0; i < groupBox.length; i++) {
    groupBoxImg[i].style.transform = 'rotate(0deg)'
    groupDepth2[i].style.height = '0';
  }
  openCount = -1;
}







/*노선등록*/
routeCreateBtn.addEventListener('click', openRouteCreate)
groupMenagementCloseBtn.addEventListener('click', closeRouteCreate)

function openRouteCreate() {
  popupAreaModulesRouteCreate.style.display = "flex"
  editOpenCount = true
}

function closeRouteCreate() {
  popupAreaModulesRouteCreate.style.display = "none"
}



/*노선등록 모두체크*/
routePopupDataDriveDateCreate[0].addEventListener('change', allchecked)

function allchecked() {
  if (routePopupDataDriveDateCreate[0].checked) {
    for (i = 1; i < 8; i++) {
      routePopupDataDriveDateCreate[i].checked = true;
    }

  } else {
    for (i = 1; i < 8; i++) {
      routePopupDataDriveDateCreate[i].checked = false;
    }
  }
}

for (i = 1; i < 8; i++) {
  routePopupDataDriveDateCreate[i].addEventListener('change', changeAllCheck)
}

function changeAllCheck() {
  if (routePopupDataDriveDateCreate[1].checked && routePopupDataDriveDateCreate[2].checked && routePopupDataDriveDateCreate[3].checked && routePopupDataDriveDateCreate[4].checked && routePopupDataDriveDateCreate[5].checked && routePopupDataDriveDateCreate[6].checked && routePopupDataDriveDateCreate[7].checked) {
    routePopupDataDriveDateCreate[0].checked = true;
  } else {
    routePopupDataDriveDateCreate[0].checked = false;
  }
}




/*그룹관리 그룹내 노선*/

for (i = 0; i < groupBoxImg.length; i++) {
  groupBoxImg[i].addEventListener('click', openGroupInside)
  groupBoxTitle[i].addEventListener('click', openGroupInside)
}

let openCount = -1;

function openGroupInside() {
  if (editOpenCount) {
    if (openCount !== Array.from(groupBox).indexOf(this.parentNode)) {
      for (i = 0; i < groupBox.length; i++) {
        groupBoxImg[i].style.transform = 'rotate(0deg)'
        groupDepth2[i].style.height = '0';
      }
      this.parentNode.querySelector("img").style.transform = 'rotate(180deg)'
      this.parentNode.parentNode.querySelector('.groupDepth2').style.height = 'auto';
      openCount = Array.from(groupBox).indexOf(this.parentNode);
    } else {
      for (i = 0; i < groupBox.length; i++) {
        groupBoxImg[i].style.transform = 'rotate(0deg)'
        groupDepth2[i].style.height = '0';
      }
      openCount = -1;
    }
  }
}




/*그룹수정*/

for (i = 0; i < editIcon.length; i++) {
  editIcon[i].addEventListener('click', ableToSave)
}

function ableToSave() {
  editOpenCount = false
  this.parentNode.parentNode.querySelectorAll('.groupBoxTitle')[0].removeAttribute("readonly")
  this.parentNode.parentNode.querySelectorAll('.groupBoxTitle')[0].style.cursor = "Auto";
  this.parentNode.parentNode.querySelectorAll('.groupBoxTitle')[0].style.outline = "inherit";
  this.parentNode.parentNode.querySelector('.groupBoxTitle').style.border = '0.1rem solid #191919';
  createGroupDataArea.querySelector('form:nth-child(2)').action = '/dispatch/regularly/group/edit'
}


for (i = 0; i < deletIcon.length; i++) {
  deletIcon[i].addEventListener('click', deletGroup)
}

function deletGroup() {
  this.parentNode.parentNode.querySelectorAll('.groupBoxTitleHidden').disabled = false;
  editOrDelete.action = '/dispatch/regularly/group/delete'
  groupSave = false
  groupDelet = true
}


btnModulesGroupSave.addEventListener('click', saveGroup)

function saveGroup() {
  editOrDelete.action = '/dispatch/regularly/group/edit'
  groupSave = true
  groupDelet = false
}


editOrDelete.addEventListener('submit', submitGroup)

function submitGroup(event) {
  if (groupDelet) {
    if (!confirm('정말로 삭제하시겠습니까?')) {
      event.preventDefault();
    }
  }
}





//삭제알림
let checkBoxCheking = false;

for (i = 0; i < groupCheck.length; i++) {
  groupCheck[i].addEventListener('change', checking)
}

function checking() {
  checkBoxCheking = false
  for (i = 0; i < groupCheck.length; i++) {
    if (groupCheck[i].checked) {
      checkBoxCheking = true
    }
  }
}


groupListForm.addEventListener('submit', deleteData)

function deleteData(e) {
  if (!checkBoxCheking) {
    e.preventDefault()
    alert('삭제할 차량을 선택해 주세요.')
  } else {
    if (confirm('정말로 삭제하시겠습니까?') == false) {
      e.preventDefault()
    }
  }
}


//유효성 검사
groupMenagementCreateBtn.addEventListener('click', fillchecker)
function fillchecker(e) {
  if (routePopupDataDriveDateCreate[0].checked == false && routePopupDataDriveDateCreate[1].checked == false && routePopupDataDriveDateCreate[2].checked == false && routePopupDataDriveDateCreate[3].checked == false && routePopupDataDriveDateCreate[4].checked == false && routePopupDataDriveDateCreate[5].checked == false && routePopupDataDriveDateCreate[6].checked == false && routePopupDataDriveDateCreate[7].checked == false) {
    e.preventDefault()
    alert('운행요일을 체크해 주세요')
  } else if (routePopupDataDriveTime[2].value.replace(/\:/g, "") >= routePopupDataDriveTime[3].value.replace(/\:/g, "")) {
    e.preventDefault()
    alert('운행시간을 다시 확인해 주세요')
  }else if(routePopupDataContractPeriod[2].value.replace(/\-/g, "") >= routePopupDataContractPeriod[3].value.replace(/\-/g, "") && routePopupDataContractPeriod[2].value !== "" && routePopupDataContractPeriod[3].value !== ""){
    e.preventDefault()
    alert('계약기간을 다시 확인해 주세요')
  }
}
routePopupSaveBtn.addEventListener('click', fillcheckerSave)
function fillcheckerSave(e) {
  if (routePopupDataDriveDateEdit[0].checked == false && routePopupDataDriveDateEdit[1].checked == false && routePopupDataDriveDateEdit[2].checked == false && routePopupDataDriveDateEdit[3].checked == false && routePopupDataDriveDateEdit[4].checked == false && routePopupDataDriveDateEdit[5].checked == false && routePopupDataDriveDateEdit[6].checked == false && routePopupDataDriveDateEdit[7].checked == false) {
    e.preventDefault()
    alert('운행요일을 체크해 주세요')
    for(i=0; i<8; i++){
      console.log(routePopupDataDriveDateEdit[i].checked)
    }
  } else if (routePopupDataDriveTime[0].value.replace(/\:/g, "") >= routePopupDataDriveTime[1].value.replace(/\:/g, "")) {
    e.preventDefault()
    alert('운행시간을 다시 확인해 주세요')
  }else if(routePopupDataContractPeriod[0].value.replace(/\-/g, "") >= routePopupDataContractPeriod[1].value.replace(/\-/g, "") && routePopupDataContractPeriod[2].value !== "" && routePopupDataContractPeriod[3].value !== ""){
    e.preventDefault()
    alert('계약기간을 다시 확인해 주세요')
  }
}





// , 추가
Array.from(routePopupDataDriverPay)[0].addEventListener('change', addComma)
Array.from(routePopupDataContractAmount)[0].addEventListener('change', addComma)
Array.from(routePopupDataDriverPay)[1].addEventListener('change', addComma)
Array.from(routePopupDataContractAmount)[1].addEventListener('change', addComma)
let onlyNumber = /[^0-9]/g;

function addComma() {
  this.value = this.value.replace(onlyNumber, "")
  this.value = this.value.replace(/\,/g, "")
  this.value = this.value.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

//전화번호 유효성
Array.from(routePopupPhoneNumber)[0].addEventListener('change', phoneNumCheckerEdit)
Array.from(routePopupPhoneNumber)[1].addEventListener('change', phoneNumChecker)

function phoneNumChecker(){
  this.value = this.value.replace(onlyNumber, "")
  if(this.value.length <= 8 || this.value.length >= 12){
    alert("형식에 맞지않는 전화번호 입니다.")
    this.value = ""
  }
  this.value = this.value.replace(/^(\d{2,3})(\d{3,4})(\d{4})$/, `$1-$2-$3`)
}
function phoneNumCheckerEdit(){
  this.value = this.value.replace(onlyNumber, "")
  if(this.value.length <= 8 || this.value.length >= 12){
    alert("형식에 맞지않는 전화번호 입니다.")
  }
  this.value = this.value.replace(/^(\d{2,3})(\d{3,4})(\d{4})$/, `$1-$2-$3`)
}