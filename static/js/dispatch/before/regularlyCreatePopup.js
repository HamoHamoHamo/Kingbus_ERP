const regularlyDispatchBtn = document.querySelectorAll(".regularlyDispatchBtn")
const popupAreaModules = document.querySelector(".popupAreaModules")
const popupBgModules = document.querySelector(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
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
const dispatchList = document.querySelectorAll(".regularyCreatePopupTbody td:nth-child(1) div")
const dispatchBoxList = document.querySelectorAll(".regularyCreatePopupTbody td:nth-child(1)")
const thisTr = document.querySelectorAll(".tableBody tr")
const filterDate = document.querySelector(".dateFilterBox input")
const GoToWork = document.querySelectorAll(".GoToWork")
const work = document.querySelectorAll(".work")
const backToHome = document.querySelectorAll(".backToHome")


let saveClass = ""
let needStart = ""
let needEnd = ""
let useDriver = ""
let addDispatchBtn = ""
let addDispatchTime = ""
let addDispatchChecker = 0
let overBusCount = true
let busCount = ""

for (i = 0; i < regularlyDispatchBtn.length; i++) {
  regularlyDispatchBtn[i].addEventListener("click", openPopup)
}

//배차팝업 열기
function openPopup() {
  popupAreaModules.style.display = "block"

  saveClass = this.parentNode.className;

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
  for (i = 0; i < thisTr.length; i++) {
    if (thisTr[i].classList.contains(`${saveClass}`)) {
      addDispatchBtn = thisTr[i].children[7].children[0]
      addDispatchTime = thisTr[i].children[7].children[0].parentNode.parentNode.children[3].innerText
    }
  }
  needStart = addDispatchTime.split("~")[0].replace(/\ |:/g, "")
  needEnd = addDispatchTime.split("~")[1].replace(/\ |:/g, "")
  for (i = 0; i < dispatchList.length; i++) {
    if (!(vehicleConnect[Object.keys(vehicleConnect)[i]] == "")) {
      if (!(vehicleConnect[Object.keys(vehicleConnect)[i]][0][1].substr(11, 5).replace(/\:/g, "") < needStart) &&
        !(vehicleConnect[Object.keys(vehicleConnect)[i]][0][0].substr(11, 5).replace(/\:/g, "") > needEnd)) {
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
    if (dispatchBoxList[i].classList.contains(`${connectData[this.parentNode.className][0]}`)) {
      dispatchBoxList[i].children[0].style.backgroundColor = "#0069D9"
      dispatchBoxList[i].children[0].style.color = "white"
      dispatchBoxList[i].children[0].style.pointerEvents = "auto"
      dispatchBoxList[i].children[0].classList.remove("addDriver")
      dispatchBoxList[i].children[0].classList.add("removeDriver")
      const newInput = document.createElement('input');
      newInput.setAttribute("type", "hidden");
      newInput.setAttribute("value", dispatchBoxList[i].className);
      newInput.setAttribute("name", 'vehicle');
      newInput.setAttribute("class", `vehicle`);
      popupContainer.appendChild(newInput);
    }
  }

  dispatchHidden.value = saveClass

  //차량대수 추가배차 가능여부 판단
  addDispatchChecker = 0

  for (i = 0; i < thisTr.length; i++) {
    if (thisTr[i].classList.contains(`${saveClass}`)) {
      busCount = thisTr[i].children[6].innerText.split("/")[1]
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
  addDispatchChecker = 0
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

      const newInput = document.createElement('input');
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
  for (i = 0; i < thisTr.length; i++) {
    if (thisTr[i].classList.contains(`${dispatchHidden.value}`)) {
      thisTr[i].children[6].innerText = `${addDispatchChecker}/${thisTr[i].children[6].innerText.split("/")[1]}`
    }
  }

}




popupBgModules.addEventListener("click", closedPopup)
SidemenuUseClose.addEventListener("click", closedPopup)
dispatchCloseBtn.addEventListener("click", closedPopup)

function closedPopup() {
  if (popupAreaModules.style.display == "block") {
    popupAreaModules.style.display = "none"
    for (i = 0; i < dispatchBoxList.length; i++) {
      dispatchBoxList[i].children[0].classList.add('addDriver');
      dispatchBoxList[i].children[0].classList.remove('removeDriver');
      dispatchBoxList[i].children[0].style.backgroundColor = 'white'
      dispatchBoxList[i].children[0].style.color = '#0069D9'
    }
    location.reload();
  } else {
    popupAreaModules.style.display = "none"
    for (i = 0; i < dispatchBoxList.length; i++) {
      dispatchBoxList[i].children[0].classList.add('addDriver');
      dispatchBoxList[i].children[0].classList.remove('removeDriver');
      dispatchBoxList[i].children[0].style.backgroundColor = 'white'
      dispatchBoxList[i].children[0].style.color = '#0069D9'
    }
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


