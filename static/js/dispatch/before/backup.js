const regularlyDispatchBtn = document.querySelectorAll(".regularlyDispatchBtn")
const popupAreaModules = document.querySelector(".popupAreaModules")
const popupBgModules = document.querySelector(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const regularyCreatePopupResult = document.querySelector(".regularyCreatePopupResult")
const regularyCreatePopupResultDiv = document.querySelectorAll(".regularyCreatePopupResult div")
const dispatchVehicle = document.querySelectorAll(".regularyCreatePopupTbody tr td:nth-child(1) div")
const routeDetail = document.querySelectorAll(".tableBody td:nth-child(3)")
const bus_count = document.querySelectorAll(".tableBody td:nth-child(7)")
const popupAreaModulesRoute = document.querySelector(".popupAreaModulesRoute")
const popupBgModulesRoute = document.querySelector(".popupBgModulesRoute")
const routePopupCloseBtn = document.querySelector(".routePopupBtnBox .btnModules:nth-child(1)")
const routePopupEditBtn = document.querySelector(".routePopupBtnBox .btnModules:nth-child(2)")
const routePopupSaveBtn = document.querySelector(".routePopupBtnBox input")
const routePoppupDetail = document.querySelector(".popupAreaModulesRoute .routePopupDataArea:nth-child(3)")
const routePoppupEdit = document.querySelector(".popupAreaModulesRoute .routePopupDataArea:nth-child(4)")
const routePopupTitle = document.querySelector(".routePopupTitle")
const dispatchCloseBtn = document.querySelector(".regularyCreatePopupBtnBox div:nth-child(1)")
const popupContainer = document.querySelector(".popupContainer")
const routePopupData = document.querySelectorAll(".routePopupData")
const dispatchHidden = document.querySelector(".dispatchHidden")
const regularyCreatePopupTbody = document.querySelector(".regularyCreatePopupTbody")
const dispatchList = document.querySelectorAll(".regularyCreatePopupTbody td:nth-child(1)")
const thisTr = document.querySelectorAll(".tableBody tr")
const filterDate = document.querySelector(".dateFilterBox input")
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
    for (i = 0; i < thisTr.length; i++) {
      if (thisTr[i].className == dispatchHidden.value) {
        searchTr = thisTr[i]
      }
    }
    let needDispatch = searchTr.querySelector("td:nth-child(7)").innerText.split('/')[1]
    const countRemoveDriver = this.parentNode.parentNode.parentNode.querySelectorAll(".removeDriver")
    if (countRemoveDriver.length < needDispatch) {
      this.style.backgroundColor = '#0069D9'
      this.style.color = 'white'

      const newDiv = document.createElement('div');
      newDiv.setAttribute("class", `${this.parentNode.className} addVehicle`);
      const newText = document.createTextNode(this.innerText);
      newDiv.appendChild(newText);
      regularyCreatePopupResult.appendChild(newDiv);

      const newinput= document.createElement('input');
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

window.onload = noMoreDispatch()
function noMoreDispatch() {
  let compare = []
  for (i = 0; i < bus_count.length; i++) {
    compare = String(bus_count[i].innerText).split("/")
    if (compare[0] == compare[1]) {
      regularlyDispatchBtn[i].style.backgroundColor = "#707070"
    }
  }
}



/*배차등록 팝업 띄우기/닫기 */
for (i = 0; i < regularlyDispatchBtn.length; i++) {
  regularlyDispatchBtn[i].addEventListener("click", openRegularlyDispatch)
}

function openRegularlyDispatch() {

  popupAreaModules.style.display = "block"

  //배차 불가차량 판별
  let departureTime = ""
  let arrivalTime = ""
  let departureTimeCheck = ""
  let arrivalTimeCheck = ""
  let cantDispatch = 0
  let filterDateNum = filterDate.value.replace(/-|T|:|\s/g, "")
  for (i = 0; i < thisTr.length; i++) {
    if (thisTr[i].className == this.parentNode.className) {
      departureTime = filterDateNum + regDatas[thisTr[i].childNodes[5].className].departure_time.replace(/-|T|:|\s/g, "")
      arrivalTime = filterDateNum + regDatas[thisTr[i].childNodes[5].className].arrival_time.replace(/-|T|:|\s/g, "")

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
        dispatchVehicle[j].parentNode.style.pointerEvents = "auto"
        const newDiv = document.createElement('div');
        newDiv.setAttribute("class", `${dispatchVehicle[j].parentNode.className} addVehicle`);
        const newText = document.createTextNode(dispatchVehicle[j].innerText);
        newDiv.appendChild(newText);
        regularyCreatePopupResult.appendChild(newDiv);

        const newinput= document.createElement('input');
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
}

popupBgModulesRoute.addEventListener("click", closedRoutePopup)
SidemenuUseClose.addEventListener("click", closedRoutePopup)
routePopupCloseBtn.addEventListener("click", closedRoutePopup)

function closedRoutePopup() {
  popupAreaModulesRoute.style.display = "none"
}


