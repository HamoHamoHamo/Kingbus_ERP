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
const groupCheck = document.querySelectorAll(".tableBody td:nth-child(1) input")
const dispatchListForm = document.querySelector(".dispatchListForm")
const dispatchHidden = document.querySelector(".dispatchHidden")
const dispatchNum = document.querySelectorAll(".orderDispatch div span")
const thisTr = document.querySelectorAll(".tableCell .table tbody tr")
const thisOtherTr = document.querySelectorAll(".tableCellScroll .table tbody tr")
const dispatchList = document.querySelectorAll(".regularyCreatePopupTbody td:nth-child(1)")
const orderDispatchDiv = document.querySelectorAll(".orderDispatchDiv")
const bus_count = document.querySelectorAll(".tableCellScroll td:nth-child(2)")
const popupContainer = document.querySelector(".popupContainer")
const GoToWork = document.querySelectorAll(".GoToWork")
const work = document.querySelectorAll(".work")
const backToHome = document.querySelectorAll(".backToHome")


/*배차등록 추가/삭제 */
for (i = 0; i < dispatchVehicle.length; i++) {
  dispatchVehicle[i].addEventListener("click", addVehicle)
}

function addVehicle() {
  if (this.className == 'addDriver') {
    let searchTr = ""
    for (i = 0; i < thisOtherTr.length; i++) {
      if (thisOtherTr[i].className == dispatchHidden.value) {
        searchTr = thisOtherTr[i]
      }
    }
    let needDispatch = searchTr.querySelector("td:nth-child(2)").innerText.split('/')[1]
    const countRemoveDriver = this.parentNode.parentNode.parentNode.querySelectorAll(".removeDriver")
    if (countRemoveDriver.length < needDispatch) {

      this.style.backgroundColor = '#0069D9'
      this.style.color = 'white'

      const newDiv = document.createElement('div');
      newDiv.setAttribute("class", `${this.parentNode.className} addVehicle`);
      const newText = document.createTextNode(this.innerText);
      newDiv.appendChild(newText);
      regularyCreatePopupResult.appendChild(newDiv);

      const newInput = document.createElement('input');
      newInput.setAttribute("type", "hidden");
      newInput.setAttribute("value", this.parentNode.className);
      newInput.setAttribute("name", 'vehicle');
      newInput.setAttribute("class", `vehicle${this.id}`);
      regularyCreatePopupResult.appendChild(newInput);
      this.classList.add('removeDriver');
      this.classList.remove('addDriver');
    }
  } else {
    removeItHidden = regularyCreatePopupResult.querySelectorAll("input");
    for (i = 0; i < removeItHidden.length; i++) {
      if (removeItHidden[i].value == this.parentNode.className) {
        removeItHidden[i].previousSibling.remove();
        removeItHidden[i].remove();
      }
    }
    this.style.backgroundColor = 'white'
    this.style.color = '#191919'
    this.classList.add('addDriver');
    this.classList.remove('removeDriver');
  }


  if (regularyCreatePopupResult.childElementCount > 6) {
    regularyCreatePopupResult.style.justifyContent = 'flex-start'
  } else {
    regularyCreatePopupResult.style.justifyContent = 'center'
  }
}



//추가 배차여부 판단
popupContainer.addEventListener('submit', noMoreDispatch)

function noMoreDispatch() {
  let compare = []
  for (i = 1; i < bus_count.length; i++) {
    compare = String(bus_count[i].innerText).split("/")
    if (compare[0] == compare[1]) {
      orderDispatchDiv[i - 1].style.backgroundColor = "#707070"
    }
  }
}





/*배차등록 팝업 띄우기/닫기 */
for (i = 0; i < orderDispatch.length; i++) {
  orderDispatch[i].addEventListener("click", openRegularlyDispatch)
}

function openRegularlyDispatch() {
  popupAreaModules.style.display = "block"
  //배차 불가차량 판별
  let departureTime = ""
  let arrivalTime = ""
  let departureTimeCheck = ""
  let arrivalTimeCheck = ""
  let cantDispatch = 0
  for (i = 0; i < thisTr.length; i++) {
    if (thisTr[i].className == this.parentNode.className) {
      departureTime = regDatas[thisTr[i].childNodes[5].className.substr(10,)].departure_date.replace(/-|T|:|\s/g, "")
      arrivalTime = regDatas[thisTr[i].childNodes[5].className.substr(10,)].arrival_date.replace(/-|T|:|\s/g, "")
    }
  }
  let = keyArray = Object.keys(vehicleConnect)
  //차량
  for (i = 0; i < dispatchList.length; i++) {
    dispatchList[i].style.pointerEvents = "auto"
    if (keyArray[i] == dispatchList[i].className) {
      if (vehicleConnect[keyArray[i]].length !== 0) {
        for (j = 0; j < vehicleConnect[keyArray[i]].length; j++) {
          cantDispatch = 0
          departureTimeCheck = vehicleConnect[keyArray[i]][j][0].replace(/-|T|:|\s/g, "")
          arrivalTimeCheck = vehicleConnect[keyArray[i]][j][1].replace(/-|T|:|\s/g, "")
          if (arrivalTimeCheck < departureTime || departureTimeCheck > arrivalTime) {
            cantDispatch = cantDispatch
          } else {
            cantDispatch = cantDispatch + 1
          }
          if (cantDispatch !== 0) {
            dispatchList[i].childNodes[1].style.backgroundColor = "#a7a7a7"
            dispatchList[i].style.pointerEvents = "none"
          }
        }
      }
    }
  }
  //기존 배차차량 띄우기
  dispatchHidden.value = this.parentNode.className;
  for (i = 0; i < connectData[this.parentNode.className].length; i++) {
    for (j = 0; j < dispatchVehicle.length; j++) {
      if (dispatchVehicle[j].parentNode.className == connectData[this.parentNode.className][i]) {
        dispatchVehicle[j].classList.remove("addDriver")
        dispatchVehicle[j].classList.add("removeDriver")
        dispatchVehicle[j].style.backgroundColor = '#0069D9'
        dispatchVehicle[j].style.color = 'white'
        dispatchVehicle[j].style.pointerEvents = "auto"
        const newDiv = document.createElement('div');
        newDiv.setAttribute("class", `${dispatchVehicle[j].parentNode.className} addVehicle`);
        const newText = document.createTextNode(dispatchVehicle[j].innerText);
        newDiv.appendChild(newText);
        regularyCreatePopupResult.appendChild(newDiv);

        const newInput = document.createElement('input');
        newInput.setAttribute("type", "hidden");
        newInput.setAttribute("value", dispatchVehicle[j].parentNode.className);
        newInput.setAttribute("name", 'vehicle');
        newInput.setAttribute("class", `vehicle${this.id}`);
        regularyCreatePopupResult.appendChild(newInput);
      }
    }
  }

  //빈 배차 색 없애기
  for(i=0; i<GoToWork.length; i++){
    if(GoToWork[i].innerText == "0"){
      GoToWork[i].style.backgroundColor = "white"
      GoToWork[i].innerText = ""
    }
    if(work[i].innerText == "0"){
      work[i].style.backgroundColor = "white"
      work[i].innerText = ""
    }
    if(backToHome[i].innerText == "0"){
      backToHome[i].style.backgroundColor = "white"
      backToHome[i].innerText = ""
    }
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
  orderDispatchData[1].innerText = regDatas[this.className.substr(10,)].bus_cnt;
  orderDispatchData[2].innerText = regDatas[this.className.substr(10,)].arrival;
  orderDispatchData[3].innerText = regDatas[this.className.substr(10,)].bus_type;
  orderDispatchData[4].innerText = regDatas[this.className.substr(10,)].operation_type;
  orderDispatchData[5].innerText = `${regDatas[this.className.substr(10,)].departure_date} ~ ${regDatas[this.className.substr(10,)].arrival_date}`;
  orderDispatchData[6].innerText = regDatas[this.className.substr(10,)].contract_status;
  orderDispatchData[7].innerText = regDatas[this.className.substr(10,)].cost_type;
  orderDispatchData[8].innerText = regDatas[this.className.substr(10,)].references;
  orderDispatchData[9].innerText = regDatas[this.className.substr(10,)].customer;
  orderDispatchData[10].innerText = regDatas[this.className.substr(10,)].customer_phone;
  orderDispatchData[11].innerText = regDatas[this.className.substr(10,)].price;
  orderDispatchData[12].innerText = regDatas[this.className.substr(10,)].deposit_status;
  orderDispatchData[13].innerText = regDatas[this.className.substr(10,)].deposit_date;
  orderDispatchData[14].innerText = regDatas[this.className.substr(10,)].bill_date;
  orderDispatchData[15].innerText = regDatas[this.className.substr(10,)].collection_type;
  orderDispatchData[16].innerText = regDatas[this.className.substr(10,)].driver_allowance;
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
  routeOrderPrice.value = regDatas[this.className.substr(10,)].price;
  routeOrderDepositStatus.value = regDatas[this.className.substr(10,)].deposit_status;
  routeOrderDepositDate.value = regDatas[this.className.substr(10,)].deposit_date;
  routeOrderBillDate.value = regDatas[this.className.substr(10,)].bill_date;
  routeOrderCollectionType.value = regDatas[this.className.substr(10,)].collection_type;
  routeOrderDriverAllowance.value = regDatas[this.className.substr(10,)].driver_allowance;
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
  noMoreDispatch()
}