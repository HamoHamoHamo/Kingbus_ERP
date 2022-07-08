const regularlyDispatchBtn = document.querySelectorAll(".regularlyDispatchBtn")
const popupAreaModules = document.querySelector(".popupAreaModules")
const popupBgModules = document.querySelector(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const regularyCreatePopupResult = document.querySelector(".regularyCreatePopupResult")
const regularyCreatePopupResultDiv = document.querySelectorAll(".regularyCreatePopupResult div")
const dispatchVehicle = document.querySelectorAll(".regularyCreatePopupTbody tr td:nth-child(1) div")
const routeDetail = document.querySelectorAll(".tableBody td:nth-child(3)")
const popupAreaModulesRoute = document.querySelector(".popupAreaModulesRoute")
const popupBgModulesRoute = document.querySelector(".popupBgModulesRoute")
const routePopupCloseBtn = document.querySelector(".routePopupBtnBox .btnModules:nth-child(1)")
const routePopupEditBtn = document.querySelector(".routePopupBtnBox .btnModules:nth-child(2)")
const routePopupSaveBtn = document.querySelector(".routePopupBtnBox input")
const routePoppupDetail = document.querySelector(".popupAreaModulesRoute .routePopupDataArea:nth-child(3)")
const routePoppupEdit = document.querySelector(".popupAreaModulesRoute .routePopupDataArea:nth-child(4)")
const routePopupTitle = document.querySelector(".routePopupTitle")
const dispatchCloseBtn = document.querySelector(".regularyCreatePopupBtnBox div:nth-child(1)")
const routePopupData = document.querySelectorAll(".routePopupData")
const routePopupDataGroupOption = document.querySelectorAll(".routePopupDataGroup option")
const routePopupDataDriveTime = document.querySelectorAll(".routePopupDataDriveTime input")
const routePopupDataRoutName = document.querySelectorAll(".routePopupDataRoutName")
const routePopupDataDriverNumber = document.querySelector(".routePopupDataDriverNumber")
const routePopupDataDriverPay = document.querySelector(".routePopupDataDriverPay")
const routePopupDataBusKindsOption = document.querySelectorAll(".routePopupDataBusKinds option")
const routePopupDataBusCount = document.querySelector(".routePopupDataBusCount")
const routePopupDataContractPeriod = document.querySelectorAll(".routePopupDataContractPeriod input")
const routePopupDatAaccount = document.querySelector(".routePopupDatAaccount")
const routePopupPhoneNumber = document.querySelector(".routePopupPhoneNumber")
const routePopupDataContractAmount = document.querySelector(".routePopupDataContractAmount")
const routePopupWorkInput = document.querySelectorAll(".routePopupWork input")
const routePopupWorkLabel = document.querySelector(".routePopupWork label:nth-child(2)")
const routePopupDataReference = document.querySelector(".routePopupDataReference")
const routePopupDataDriveDateEdit = document.querySelectorAll(".routePopupDataDriveDate input")
const routePopupDataDriveDateEditLabel = document.querySelectorAll(".routePopupDataDriveDate label")
const sendToHidden = document.querySelector(".sendToHidden")





/*배차등록 추가/삭제 */
for (i = 0; i < dispatchVehicle.length; i++) {
  dispatchVehicle[i].addEventListener("click", addVehicle)
}

function addVehicle() {
  if (this.className == 'addDriver') {

    this.style.backgroundColor = '#0069D9'
    this.style.color = 'white'

    const newDiv = document.createElement('div');
    newDiv.setAttribute("class", `vehicle${this.id} addVehicle`);
    const newText = document.createTextNode(this.innerText);
    newDiv.appendChild(newText);
    regularyCreatePopupResult.appendChild(newDiv);

    const newInput = document.createElement('input');
    newInput.setAttribute("type", "hidden");
    newInput.setAttribute("value", `vehicle${this.id}`);
    newInput.setAttribute("name", 'vehicle');
    newInput.setAttribute("class", `vehicle${this.id}`);
    regularyCreatePopupResult.appendChild(newInput);

    this.classList.add('removeDriver');
    this.classList.remove('addDriver');
  } else {
    const removeIt = document.querySelectorAll(`.vehicle${this.id}`)
    removeIt[0].remove();
    removeIt[1].remove();
    this.style.backgroundColor = 'white'
    this.style.color = '#191919'
    this.classList.add('addDriver');
    this.classList.remove('removeDriver');
  }


  if (regularyCreatePopupResult.childElementCount > 6) {
    regularyCreatePopupResult.style.justifyContent = 'flex-start'
    console.log('check')
  } else {
    regularyCreatePopupResult.style.justifyContent = 'center'
  }
}




/*배차등록 팝업 띄우기/닫기 */
for (i = 0; i < regularlyDispatchBtn.length; i++) {
  regularlyDispatchBtn[i].addEventListener("click", openRegularlyDispatch)
}

function openRegularlyDispatch() {
  popupAreaModules.style.display = "block"
}



popupBgModules.addEventListener("click", closedRegularlyDispatchBg)
SidemenuUseClose.addEventListener("click", closedRegularlyDispatchSideMenu)
dispatchCloseBtn.addEventListener("click", closedRegularlyDispatchBtn)

function closedRegularlyDispatchBg() {
  popupAreaModules.style.display = "none"
  regularyCreatePopupResult.textContent = '';
  for (i = 0; i < dispatchVehicle.length; i++) {
    dispatchVehicle[i].classList.add('addDriver');
    dispatchVehicle[i].classList.remove('removeDriver')
    dispatchVehicle[i].style.backgroundColor = 'white'
    dispatchVehicle[i].style.color = '#191919'
  }
}
function closedRegularlyDispatchSideMenu() {
  popupAreaModules.style.display = "none"
  regularyCreatePopupResult.textContent = '';
  for (i = 0; i < dispatchVehicle.length; i++) {
    dispatchVehicle[i].classList.add('addDriver');
    dispatchVehicle[i].classList.remove('removeDriver')
    dispatchVehicle[i].style.backgroundColor = 'white'
    dispatchVehicle[i].style.color = '#191919'
  }
}
function closedRegularlyDispatchBtn() {
  popupAreaModules.style.display = "none"
  regularyCreatePopupResult.textContent = '';
  for (i = 0; i < dispatchVehicle.length; i++) {
    dispatchVehicle[i].classList.add('addDriver');
    dispatchVehicle[i].classList.remove('removeDriver')
    dispatchVehicle[i].style.backgroundColor = 'white'
    dispatchVehicle[i].style.color = '#191919'
  }
}



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
  if (routePopupWorkLabel.innerText == regDatas[this.className].work_type) {
    routePopupWorkInput[0].checked = true;
  } else {
    routePopupWorkInput[1].checked = true;
  }
  routePopupDataReference.value = regDatas[this.className].references;
  let weekArray = regDatas[this.className].week.split('')
  let newWeekArray = weekArray.filter(item => item !== ' ')
  let weekAllCount = 0;
  for (i = 1; i < routePopupDataDriveDateEdit.length; i++) {
    if (newWeekArray.find(item => item == routePopupDataDriveDateEditLabel[i].innerText)) {
      console.log(routePopupDataDriveDateEdit[i])
      routePopupDataDriveDateEdit[i].checked = true;
      weekAllCount = weekAllCount + 1;
      if (weekAllCount == 7) {
        routePopupDataDriveDateEdit[0].checked = true;
      }
    }
  }
  sendToHidden.value = this.parentElement.className;
}

popupBgModulesRoute.addEventListener("click", closedRoutePopup)
SidemenuUseClose.addEventListener("click", closedRoutePopupMenu)
routePopupCloseBtn.addEventListener("click", closedRoutePopupBtn)
routePopupEditBtn.addEventListener("click", changeEdit)

function closedRoutePopup() {
  popupAreaModulesRoute.style.display = "none"
}
function closedRoutePopupMenu() {
  popupAreaModulesRoute.style.display = "none"
}
function closedRoutePopupBtn() {
  popupAreaModulesRoute.style.display = "none"
  routePopupTitle.innerText = "노선상세";
  routePoppupDetail.style.display = "flex";
  routePoppupEdit.style.display = "none";
  routePopupEditBtn.style.display = 'flex';
  routePopupSaveBtn.style.display = 'none';
}
function changeEdit() {
  routePopupTitle.innerText = "노선수정";
  routePoppupDetail.style.display = "none";
  routePoppupEdit.style.display = "flex";
  routePopupEditBtn.style.display = 'none';
  routePopupSaveBtn.style.display = 'flex';
}


/*노선상세 모두체크*/
routePopupDataDriveDateEdit[0].addEventListener('change', allchecked)

function allchecked() {
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
  routePopupDataDriveDateEdit[i].addEventListener('change', changeAllCheck)
}

function changeAllCheck() {
  if (routePopupDataDriveDateEdit[1].checked && routePopupDataDriveDateEdit[2].checked && routePopupDataDriveDateEdit[3].checked && routePopupDataDriveDateEdit[4].checked && routePopupDataDriveDateEdit[5].checked && routePopupDataDriveDateEdit[6].checked && routePopupDataDriveDateEdit[7].checked) {
    routePopupDataDriveDateEdit[0].checked = true;
  } else {
    routePopupDataDriveDateEdit[0].checked = false;
  }
}