const routeDetail = document.querySelectorAll(".tableBody td:nth-child(3)")
const popupAreaModulesRoute = document.querySelector(".popupAreaModulesRoute")
const popupBgModulesRoute = document.querySelectorAll(".popupBgModulesRoute")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const routePopupTitle = document.querySelector(".routePopupTitle")
const routePopupCloseBtn = document.querySelector(".routePopupBtnBox .btnModules:nth-child(1)")
const routePopupEditBtn = document.querySelector(".routePopupBtnBox .btnModules:nth-child(2)")
const routePopupSaveBtn = document.querySelector(".routePopupBtnBox input")
const routePoppupDetail = document.querySelector(".popupContainerRoute .routePopupDataArea:nth-child(2)")
const routePoppupEdit = document.querySelector(".popupContainerRoute .routePopupDataArea:nth-child(3)")
const routePopupDataDriveDateEdit = document.querySelectorAll(".popupAreaModulesRoute .routePopupDataDriveDate input")
const routePopupDataDriveDateCreate = document.querySelectorAll(".popupAreaModulesRouteCreate .routePopupDataDriveDate input")
const groupMenagementBtn = document.querySelector(".gruopManagementBtn")
const routeCreateBtn = document.querySelector(".createRouteBtn")
const groupMenagementCloseBtn = document.querySelector(".groupMenagementCloseBtn")
const groupMenagementCreateBtn = document.querySelector(".groupMenagementCreateBtn")
const groupCretetCloseBtn = document.querySelector(".groupCretetCloseBtn")
const popupAreaModulesRouteCreate = document.querySelector(".popupAreaModulesRouteCreate")
const popupAreaModulesGroupCreate = document.querySelector(".popupAreaModulesGroupCreate")
const groupBox = document.querySelectorAll(".groupBox")
const groupDepth2 = document.querySelectorAll(".groupDepth2")
const routePopupData = document.querySelectorAll(".routePopupData")
const routePopupDataGroupOption = document.querySelectorAll(".routePopupDataGroup option")
const routePopupDataDriveTime = document.querySelectorAll(".routePopupDataDriveTime input")
const routePopupDataRoutName = document.querySelectorAll(".routePopupDataRoutName")
const routePopupDataDriverNumber = document.querySelector(".routePopupDataDriverNumber")
const routePopupDataDriverPay = document.querySelector(".routePopupDataDriverPay")
const routePopupDataBusKindsOption = document.querySelectorAll(".routePopupDataBusKinds option")
const routePopupDataBusCount = document.querySelector(".routePopupDataBusCount")
const routePopupDataContractPeriod = document.querySelectorAll(".routePopupDataContractPeriod")
const routePopupDatAaccount = document.querySelector(".routePopupDatAaccount")
const routePopupPhoneNumber = document.querySelector(".routePopupPhoneNumber")
const routePopupDataContractAmount = document.querySelector(".routePopupDataContractAmount")
const routePopupWorkInput = document.querySelectorAll(".routePopupWork input")
const routePopupWorkLabel = document.querySelector(".routePopupWork label:nth-child(2)")
const routePopupDataReference = document.querySelector(".routePopupDataReference")



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
  routePopupData[6].innerText = regDatas[this.className].driver_allowance
  routePopupData[7].innerText = regDatas[this.className].bus_type
  routePopupData[8].innerText = regDatas[this.className].bus_cnt
  routePopupData[9].innerText = regDatas[this.className].customer
  routePopupData[10].innerText = regDatas[this.className].customer_phone
  routePopupData[11].innerText = regDatas[this.className].price
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
  routePopupDataDriverPay.value = regDatas[this.className].driver_allowance;
  for (i = 0; i < routePopupDataBusKindsOption.length; i++) {
    if (routePopupDataBusKindsOption[i].innerText == regDatas[this.className].bus_type) {
      routePopupDataBusKindsOption[i].selected = true;
    }
  }
  routePopupDataBusCount.value = regDatas[this.className].bus_cnt;
  routePopupDatAaccount.value = regDatas[this.className].customer;
  routePopupPhoneNumber.value = regDatas[this.className].customer_phone;
  routePopupDataContractAmount.value = regDatas[this.className].price;
  routePopupDataContractPeriod[0].value = regDatas[this.className].contract_start_date;
  routePopupDataContractPeriod[1].value = regDatas[this.className].contract_end_date;
  if(routePopupWorkLabel.innerText == regDatas[this.className].work_type){
    routePopupWorkInput[0].checked = true;
  }else{
    routePopupWorkInput[1].checked = true;
  }
  routePopupDataReference.value = regDatas[this.className].references;
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
  popupAreaModulesGroupCreate.style.display = "flex"
}

function closeGroupMenagement() {
  popupAreaModulesGroupCreate.style.display = "none"
}







/*노선등록*/
routeCreateBtn.addEventListener('click', openRouteCreate)
groupMenagementCloseBtn.addEventListener('click', closeRouteCreate)

function openRouteCreate() {
  popupAreaModulesRouteCreate.style.display = "flex"
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
for (i = 0; i < groupBox.length; i++) {
  groupBox[i].addEventListener('click', openGroupInside)
}

let openCount = -1;

function openGroupInside() {
  if (openCount !== Array.from(groupBox).indexOf(this)) {
    for (i = 0; i < groupBox.length; i++) {
      groupBox[i].querySelector('img').style.transform = 'rotate(0deg)'
      groupBox[i].parentNode.querySelector('.groupDepth2').style.height = '0';
    }
    this.querySelector('img').style.transform = 'rotate(180deg)'
    this.parentNode.querySelector('.groupDepth2').style.height = 'auto';
    openCount = Array.from(groupBox).indexOf(this);
  } else {
    for (i = 0; i < groupBox.length; i++) {
      groupBox[i].querySelector('img').style.transform = 'rotate(0deg)'
      groupBox[i].parentNode.querySelector('.groupDepth2').style.height = '0';
    }
    openCount = -1;
  }
}
