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
const routePoppupDetail = document.querySelector(".popupContainerRoute .routePopupDataArea:nth-child(2)")
const routePoppupEdit = document.querySelector(".popupContainerRoute .routePopupDataArea:nth-child(3)")
const routePopupTitle = document.querySelector(".routePopupTitle")
const routePopupDataDriveDate = document.querySelectorAll(".routePopupDataDriveDate input")
const dispatchCloseBtn = document.querySelector(".regularyCreatePopupBtnBox div:nth-child(1)")





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
}
function changeEdit() {
  routePopupTitle.innerText = "노선수정";
  routePoppupDetail.style.display = "none";
  routePoppupEdit.style.display = "flex";
  routePopupEditBtn.style.display = 'none';
  routePopupSaveBtn.style.display = 'flex';
}


/*노선상세 모두체크*/
routePopupDataDriveDate[0].addEventListener('change', allchecked)

function allchecked() {
  if (routePopupDataDriveDate[0].checked) {
    for (i = 1; i < 8; i++) {
      routePopupDataDriveDate[i].checked = true;
    }

  } else {
    for (i = 1; i < 8; i++) {
      routePopupDataDriveDate[i].checked = false;
    }
  }
}

for (i = 1; i < 8; i++) {
  routePopupDataDriveDate[i].addEventListener('change', changeAllCheck)
}

function changeAllCheck() {
  if (routePopupDataDriveDate[1].checked && routePopupDataDriveDate[2].checked && routePopupDataDriveDate[3].checked && routePopupDataDriveDate[4].checked && routePopupDataDriveDate[5].checked && routePopupDataDriveDate[6].checked && routePopupDataDriveDate[7].checked) {
    routePopupDataDriveDate[0].checked = true;
  } else {
    routePopupDataDriveDate[0].checked = false;
  }
}