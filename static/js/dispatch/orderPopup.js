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
  } else {
    regularyCreatePopupResult.style.justifyContent = 'center'
  }
}




/*배차등록 팝업 띄우기/닫기 */
for (i = 0; i < orderDispatch.length; i++) {
  orderDispatch[i].addEventListener("click", openRegularlyDispatch)
}

function openRegularlyDispatch() {
  popupAreaModules.style.display = "block"
}


for (i = 0; i < 3; i++) {
  popupBgModules[i].addEventListener("click", closedRegularlyDispatchBg)
}
SidemenuUseClose.addEventListener("click", closedRegularlyDispatchSideMenu)
dispatchCloseBtn.addEventListener("click", closedRegularlyDispatchBtn)

function closedRegularlyDispatchBg() {
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
}
function closedRegularlyDispatchSideMenu() {
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
}

orderDetailEditBtn.addEventListener('click', changeDetail)

function changeDetail(){
  orderPopupTitle[1].innerText = '일반주문 수정'
  orderDetailEditBtn.style.display = 'none'
  orderDetailSaveBtn.style.display = 'flex'
  orderPopupDataAreaDetail.style.display = 'none'
  orderPopupDataAreaEdit.style.display = 'flex'
}

orderDetailCloseBtn.addEventListener('click', orderDetailClose)

function orderDetailClose(){
  popupAreaModulesOrderRoute.style.display = 'none'
}