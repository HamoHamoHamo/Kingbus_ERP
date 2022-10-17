const dispatchVehicle = document.querySelectorAll(".regularyCreatePopupTbody tr td:nth-child(1) div")
const regularyCreatePopupResult = document.querySelector(".regularyCreatePopupResult")
const regularyCreatePopupResultDiv = document.querySelectorAll(".regularyCreatePopupResult div")
const orderDispatch = document.querySelectorAll(".orderDispatch")
const popupAreaModules = document.querySelector(".popupAreaModules")
const popupBgModules = document.querySelectorAll(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const dispatchCloseBtn = document.querySelector(".regularyCreatePopupBtnBox div:nth-child(1)")
const createRouteBtn = document.querySelector(".createRouteBtn")
const popupAreaModulesOrder = document.querySelector(".popupAreaModulesOrder")
const dispatchCreateCloseBtn = document.querySelectorAll(".regularyCreatePopupBtnBox div")
const orderRouteDetail = document.querySelectorAll(".orderRote")
const popupAreaModulesOrderRoute = document.querySelector(".popupAreaModulesOrderRoute")
const orderPopupTitle = document.querySelectorAll(".orderPopupTitle")
const orderDetailEditBtn = document.querySelector(".orderPopupBtnBox div:nth-child(2)")
const orderDetailSaveBtn = document.querySelector(".orderPopupBtnBox input")
const orderPopupDataAreaDetail = document.querySelector(".orderPopupDataAreaDetail")
const orderPopupDataAreaEdit = document.querySelector(".orderPopupDataAreaEdit")
const orderDetailCloseBtn = document.querySelector(".orderPopupBtnBox div:nth-child(1) ")
const orderDispatchData = document.querySelectorAll(".orderDispatchData")
const routeOrderDeparture = document.querySelector(".routeOrderDeparture")
const routeOrderBusCnt = document.querySelector(".routeOrderBusCnt")
const routeOrderArrival = document.querySelector(".routeOrderArrival")
const routeOrderBusType = document.querySelector(".routeOrderBusType option")
const routeOrderOperationType = document.querySelector(".routeOrderOperationType option")
const routeOrderDepartureDate = document.querySelectorAll(".routeOrderDepartureDate input")
const routeOrderContactStatus = document.querySelector(".routeOrderContactStatus")
const routeOrderCostType = document.querySelector(".routeOrderCostType option")
const routeOrderReferences = document.querySelector(".routeOrderReferences")
const routeOrderCustomer = document.querySelector(".routeOrderCustomer")
const routeOrderCustomerPhone = document.querySelector(".routeOrderCustomerPhone")
const routeOrderPrice = document.querySelector(".routeOrderPrice")
const routeOrderDepositStatus = document.querySelector(".routeOrderDepositStatus")
const routeOrderDepositDate = document.querySelector(".routeOrderDepositDate")
const routeOrderBillDate = document.querySelector(".routeOrderBillDate")
const routeOrderCollectionType = document.querySelector(".routeOrderCollectionType")
const routeOrderDriverAllowance = document.querySelector(".routeOrderDriverAllowance")
const routeOrderPaymentMethod = document.querySelector(".routeOrderPaymentMethod input")
const routeOrderVat = document.querySelector(".routeOrderVat input")
const sendToHidden = document.querySelector(".sendToHidden")
const groupCheck = document.querySelectorAll(".tableCell tbody td:nth-child(1) input")
const dispatchListForm = document.querySelector(".dispatchListForm")
const dispatchHidden = document.querySelector(".dispatchHidden")
const dispatchNum = document.querySelectorAll(".orderDispatch div span")
const thisTr = document.querySelectorAll(".tableCell .table tbody tr")
const thisOtherTr = document.querySelectorAll(".tableCellScroll .table tbody tr")
const dispatchList = document.querySelectorAll(".regularyCreatePopupTbody td:nth-child(1) div")
const dispatchBoxList = document.querySelectorAll(".regularyCreatePopupTbody td:nth-child(1)")
const orderDispatchDiv = document.querySelectorAll(".orderDispatchDiv")
const bus_count = document.querySelectorAll(".tableCellScroll td:nth-child(2)")
const popupContainer = document.querySelector(".popupContainer")
const GoToWork = document.querySelectorAll(".GoToWork")
const work = document.querySelectorAll(".work")
const backToHome = document.querySelectorAll(".backToHome")
const orderPopupDataDriverAllowance = document.querySelector(".orderPopupDataDriverAllowance")
const orderPopupDataPrice = document.querySelector(".orderPopupDataPrice")
const dateSetting = document.querySelectorAll(".dateFilterBox input")
const driver_allowance = document.querySelector(".tableCellScroll .table tbody td:nth-child(4)")
const price = document.querySelector(".tableCellScroll .table tbody td:nth-child(6)")
const customer_phone = document.querySelector(".tableCellScroll .table tbody td:nth-child(7)")
const createPhoneNumber = document.querySelectorAll(".orderPopupDataCell input")

let saveClass = ""
let needStart = ""
let needEnd = ""
let useDriver = ""
let addDispatchBtn = ""
let addDispatchChecker = 0
let overBusCount = true
let busCount = ""

for (i = 0; i < orderDispatchDiv.length; i++) {
  orderDispatchDiv[i].addEventListener("click", openPopup)
}

//배차팝업 열기
function openPopup() {
  popupAreaModules.style.display = "block"

  saveClass = this.parentNode.parentNode.className;

  //빈 배차 색 없애기
  for (i = 0; i < GoToWork.length; i++) {
    if (GoToWork[i].innerText == "0") {
      GoToWork[i].style.backgroundColor = "white"
      GoToWork[i].innerText = ""
    }
    if (work[i].innerText == "0") {
      work[i].style.backgroundColor = "white"
      work[i].innerText = ""
    }
    if (backToHome[i].innerText == "0") {
      backToHome[i].style.backgroundColor = "white"
      backToHome[i].innerText = ""
    }
  }

  //배차불가 차량
  for (i = 0; i < thisOtherTr.length; i++) {
    if (thisOtherTr[i].classList.contains(`${saveClass}`)) {
      addDispatchBtn = thisOtherTr[i].children[0].children[0]
    }
    if (thisTr[i].classList.contains(`${saveClass}`)) {
      addDispatchTime = thisTr[i].children[1].children[2].innerText.substr(4, 11)
    }
  }
  needStart = addDispatchTime.split("~")[0].replace(/\ |:/g, "")
  needEnd = addDispatchTime.split("~")[1].replace(/\ |:/g, "")
  for (i = 0; i < dispatchList.length; i++) {
    if (!(vehicleConnect[Object.keys(vehicleConnect)[i]] == "")) {
      if (vehicleConnect[Object.keys(vehicleConnect)[i]][0][1].substr(11, 5).replace(/\:/g, "") >= needStart ||
        vehicleConnect[Object.keys(vehicleConnect)[i]][0][0].substr(11, 5).replace(/\:/g, "") <= needEnd) {
        for (j = 0; j < dispatchBoxList.length; j++) {
          if (dispatchBoxList[j].classList.contains(`${Object.keys(vehicleConnect)[i]}`)) {
            dispatchBoxList[j].children[0].style.backgroundColor = "grey"
            dispatchBoxList[j].children[0].style.pointerEvents = "none"
          }
        }
      }
    }
  }

  //기존 배차차량
  for (i = 0; i < dispatchBoxList.length; i++) {
    for (j = 0; j < connectData[saveClass].length; j++) {
      if (dispatchBoxList[i].classList.contains(`${connectData[this.parentNode.parentNode.className][j]}`)) {
        dispatchBoxList[i].children[0].style.backgroundColor = "#0069D9"
        dispatchBoxList[i].children[0].style.color = "white"
        dispatchBoxList[i].children[0].style.pointerEvents = "auto"
        dispatchBoxList[i].children[0].classList.remove("addDriver")
        dispatchBoxList[i].children[0].classList.add("removeDriver")
        const newinput= document.createElement('input');
        newInput.setAttribute("type", "hidden");
        newInput.setAttribute("value",  dispatchBoxList[i].className);
        newInput.setAttribute("name", 'vehicle');
        newInput.setAttribute("class", `vehicle`);
        popupContainer.appendChild(newInput);
      }
    }

  }

  dispatchHidden.value = saveClass
  
  //차량대수 추가배차 가능여부 판단
  addDispatchChecker = 0

  for (i = 0; i < thisOtherTr.length; i++) {
    if (thisOtherTr[i].classList.contains(`${saveClass}`)) {
      busCount = thisOtherTr[i].children[1].innerText.split("/")[1]
    }
  }
  const vehicle = document.querySelectorAll(".vehicle")
  for (i = 0; i < vehicle.length; i++) {
    addDispatchChecker = addDispatchChecker + 1
  }

  if (addDispatchChecker >= busCount) {
    overBusCount = false
  } else {
    overBusCount = true
  }
}

//배차추가
for (i = 0; i < dispatchList.length; i++) {
  dispatchList[i].addEventListener("click", pickDispatch)
}

function pickDispatch() {
  if (this.classList.contains("addDriver")) {
    if (overBusCount) {
      this.style.backgroundColor = "#0069D9"
      this.style.color = "white"
      this.classList.remove("addDriver")
      this.classList.add("removeDriver")
      const dispatchSpan = document.createElement('span');
      const disparchDriver = document.createTextNode(this.innerText);
      dispatchSpan.appendChild(disparchDriver);
      addDispatchBtn.appendChild(dispatchSpan);

      const newinput= document.createElement('input');
      newInput.setAttribute("type", "hidden");
      newInput.setAttribute("value", this.parentNode.className);
      newInput.setAttribute("name", 'vehicle');
      newInput.setAttribute("class", `vehicle`);
      popupContainer.appendChild(newInput);
    }
  } else {
    this.style.backgroundColor = "white"
    this.style.color = "black"
    this.classList.remove("removeDriver")
    this.classList.add("addDriver")
    for (i = 0; i < addDispatchBtn.children.length; i++) {
      if (addDispatchBtn.children[i].innerText == this.innerText) {
        addDispatchBtn.children[i].remove()
      }
    }
    const vehicle = document.querySelectorAll(".vehicle")
    for (i = 0; i < vehicle.length; i++) {
      if (vehicle[i].value == this.parentNode.className) {
        vehicle[i].remove()
      }
    }
  }
  const vehicle = document.querySelectorAll(".vehicle")
  for (i = 0; i < vehicle.length; i++) {
    addDispatchChecker = addDispatchChecker + 1
  }
  if (addDispatchChecker >= busCount) {
    overBusCount = false
  } else {
    overBusCount = true
  }
}



for (i = 0; i < 3; i++) {
  popupBgModules[i].addEventListener("click", closedRegularlyDispatch)
}
SidemenuUseClose.addEventListener("click", closedRegularlyDispatch)
dispatchCloseBtn.addEventListener("click", closedRegularlyDispatch)

function closedRegularlyDispatch() {
  popupAreaModules.style.display = "none"
  popupAreaModulesOrder.style.display = "none"
  popupAreaModulesOrderRoute.style.display = 'none'
  regularyCreatePopupResult.textContent = '';
  for (i = 0; i < dispatchVehicle.length; i++) {
    dispatchVehicle[i].classList.add('addDriver');
    dispatchVehicle[i].classList.remove('removeDriver')
    dispatchVehicle[i].style.backgroundColor = 'white'
    dispatchVehicle[i].style.color = '#191919'
  }
  for (j = 0; j < dispatchList.length; j++) {
    dispatchList[i].style.pointerEvents = "auto"
  }
}





/*노선등록 팝업*/
createRouteBtn.addEventListener('click', openRouteCreate)

function openRouteCreate() {
  popupAreaModulesOrder.style.display = "block"
}

dispatchCreateCloseBtn[1].addEventListener("click", dispatchCreateClose)

function dispatchCreateClose() {
  popupAreaModulesOrder.style.display = "none"
}




/*일반배차 상세*/
for (i = 0; i < orderRouteDetail.length; i++) {
  orderRouteDetail[i].addEventListener('click', openOrderDetail)
}

function openOrderDetail() {
  popupAreaModulesOrderRoute.style.display = 'block'
  orderDispatchData[0].innerText = regDatas[this.className.substr(10,)].departure;
  orderDispatchData[1].innerText = `${regDatas[this.className.substr(10,)].bus_cnt}대`;
  orderDispatchData[2].innerText = regDatas[this.className.substr(10,)].arrival;
  orderDispatchData[3].innerText = regDatas[this.className.substr(10,)].bus_type;
  orderDispatchData[4].innerText = regDatas[this.className.substr(10,)].operation_type;
  orderDispatchData[5].innerText = `${regDatas[this.className.substr(10,)].departure_date} ~ ${regDatas[this.className.substr(10,)].arrival_date}`;
  orderDispatchData[6].innerText = regDatas[this.className.substr(10,)].contract_status;
  orderDispatchData[7].innerText = regDatas[this.className.substr(10,)].cost_type;
  orderDispatchData[8].innerText = regDatas[this.className.substr(10,)].references;
  orderDispatchData[9].innerText = regDatas[this.className.substr(10,)].customer;
  orderDispatchData[10].innerText = regDatas[this.className.substr(10,)].customer_phone.replace(/^(\d{2,3})(\d{3,4})(\d{4})$/, `$1-$2-$3`);
  orderDispatchData[11].innerText = `${regDatas[this.className.substr(10,)].price.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`;
  orderDispatchData[12].innerText = regDatas[this.className.substr(10,)].deposit_status;
  orderDispatchData[13].innerText = regDatas[this.className.substr(10,)].deposit_date;
  orderDispatchData[14].innerText = regDatas[this.className.substr(10,)].bill_date;
  orderDispatchData[15].innerText = regDatas[this.className.substr(10,)].collection_type;
  orderDispatchData[16].innerText = `${regDatas[this.className.substr(10,)].driver_allowance.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`;
  if (regDatas[this.className.substr(10,)].payment_method == 'y') {
    orderDispatchData[17].innerText = '선지급'
  } else {
    orderDispatchData[17].innerText = 'x'
  }
  if (regDatas[this.className.substr(10,)].VAT == 'y') {
    orderDispatchData[18].innerText = '포함'
  } else {
    orderDispatchData[18].innerText = 'x'
  }
  routeOrderDeparture.value = regDatas[this.className.substr(10,)].departure;
  routeOrderBusCnt.value = regDatas[this.className.substr(10,)].bus_cnt;
  routeOrderArrival.value = regDatas[this.className.substr(10,)].arrival;
  routeOrderDepartureDate[0].value = regDatas[this.className.substr(10,)].departure_date;
  routeOrderDepartureDate[1].value = regDatas[this.className.substr(10,)].arrival_date;
  routeOrderContactStatus.value = regDatas[this.className.substr(10,)].contract_status;
  routeOrderReferences.value = regDatas[this.className.substr(10,)].references;
  routeOrderCustomer.value = regDatas[this.className.substr(10,)].customer;
  routeOrderCustomerPhone.value = regDatas[this.className.substr(10,)].customer_phone;
  routeOrderPrice.value = regDatas[this.className.substr(10,)].price.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  routeOrderDepositStatus.value = regDatas[this.className.substr(10,)].deposit_status;
  routeOrderDepositDate.value = regDatas[this.className.substr(10,)].deposit_date;
  routeOrderBillDate.value = regDatas[this.className.substr(10,)].bill_date;
  routeOrderCollectionType.value = regDatas[this.className.substr(10,)].collection_type;
  routeOrderDriverAllowance.value = regDatas[this.className.substr(10,)].driver_allowance.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  if (regDatas[this.className.substr(10,)].payment_method == 'y') {
    routeOrderPaymentMethod.checked = true;
  } else {
    routeOrderPaymentMethod.checked = false;
  }
  if (regDatas[this.className.substr(10,)].VAT == 'y') {
    routeOrderVat.checked = true;
  } else {
    routeOrderVat.checked = false;
  }
  for (i = 0; i < routeOrderBusType.length; i++) {
    if (routeOrderBusType[i].innerText == regDatas[this.className.substr(10,)].bus_type) {
      routeOrderBusType[i].selected = true;
    }
  }
  for (i = 0; i < routeOrderOperationType.length; i++) {
    if (routeOrderOperationType[i].innerText == regDatas[this.className.substr(10,)].operation_type) {
      routeOrderOperationType[i].selected = true;
    }
  }
  for (i = 0; i < routeOrderCostType.length; i++) {
    if (routeOrderCostType[i].innerText == regDatas[this.className.substr(10,)].cost_type) {
      routeOrderCostType[i].selected = true;
    }
  }
  sendToHidden.value = this.parentElement.className;
}

orderDetailEditBtn.addEventListener('click', changeDetail)

function changeDetail() {
  orderPopupTitle[1].innerText = '일반주문 수정'
  orderDetailEditBtn.style.display = 'none'
  orderDetailSaveBtn.style.display = 'flex'
  orderPopupDataAreaDetail.style.display = 'none'
  orderPopupDataAreaEdit.style.display = 'flex'
}

orderDetailCloseBtn.addEventListener('click', orderDetailClose)

function orderDetailClose() {
  popupAreaModulesOrderRoute.style.display = 'none'
  orderPopupTitle[1].innerText = '일반주문 상세'
  orderDetailEditBtn.style.display = 'flex'
  orderDetailSaveBtn.style.display = 'none'
  orderPopupDataAreaDetail.style.display = 'flex'
  orderPopupDataAreaEdit.style.display = 'none'
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
      console.log(checkBoxCheking)
    }
  }
}


dispatchListForm.addEventListener('submit', checkToDelete)

function checkToDelete(e) {
  if (!checkBoxCheking) {
    e.preventDefault()
    alert('삭제할 노선을 선택해 주세요.')
  } else {
    if (confirm('정말로 삭제하시겠습니까?') == false) {
      e.preventDefault()
    }
  }
}





// 배차차량 줄바꿈
let lineBreake
window.onload = function () {
  for (i = 0; i < orderDispatchDiv.length; i++) {
    if (orderDispatchDiv[i].childElementCount > 1) {
      const breake = document.createElement("br")
      lineBreake = Math.round(orderDispatchDiv[i].childElementCount);
      orderDispatchDiv[i].insertBefore(breake, orderDispatchDiv[i].childNodes[lineBreake])
    }
  }
  driver_allowance.innerText = driver_allowance.innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
  price.innerText = price.innerText.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
  customer_phone.innerText = customer_phone.innerText.replace(/^(\d{2,3})(\d{3,4})(\d{4})$/, `$1-$2-$3`)
}

orderPopupDataDriverAllowance.addEventListener('change', addComma)
orderPopupDataPrice.addEventListener('change', addComma)

let onlyNumber = /[^0-9]/g;

function addComma() {
  this.value = this.value.replace(onlyNumber, "")
  this.value = this.value.replace(/\,/g, "")
  this.value = this.value.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}


//기간 연동
dateSetting[0].addEventListener('change', changeDate)

function changeDate() {
  dateSetting[1].value = dateSetting[0].value
}

//기간 역전 방지

dateSetting[1].addEventListener('change', blockDate)

function blockDate() {
  if (dateSetting[0].value.replace(/\-/g, "") > dateSetting[1].value.replace(/\-/g, "")) {
    alert("기간을 올바르게 설정해 주세요")
    dateSetting[1].value = dateSetting[0].value
  }
}

//전화번호 형식
createPhoneNumber[8].addEventListener("change", phoneNumChecker)

function phoneNumChecker() {
  this.value = this.value.replace(onlyNumber, "")
  if (this.value.length <= 8 || this.value.length >= 12) {
    alert("형식에 맞지않는 전화번호 입니다.")
    this.value = ""
  }
  this.value = this.value.replace(/^(\d{2,3})(\d{3,4})(\d{4})$/, `$1-$2-$3`)
}