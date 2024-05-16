import { addEventClosePopup, closePopup } from "/static/js/common/popupCommon.js"
import { addEventSelectAllCheck } from "/static/js/common/checkbox.js"

// 팝업
const openPopup = document.querySelector('.openPopup');
const popupAreaModules = document.querySelectorAll('.popupAreaModules');
const createPopupTitle = document.querySelector(".createPopupTitle")
const popupCreateForm = document.querySelector(".popupCreateForm")
const createBtn = document.querySelector(".createBtn")


const deleteForm = document.querySelector(".deleteForm")

const details = document.querySelectorAll(".detail")

// 팝업 input
const popupName = document.querySelector(".popupName")
const popupAddress = document.querySelector(".popupAddress")
const popupLatitude = document.querySelector(".popupLatitude")
const popupLongitude = document.querySelector(".popupLongitude")
const popupReferences = document.querySelector(".popupReferences")
const sendToHidden = document.querySelector(".sendToHidden")
const essential = document.querySelectorAll(".essential")


//정류장상세
for (i = 0; i < details.length; i++) {
  details[i].addEventListener('click', openDetailPopup)
}

let popupStatus = 'create'

const getDetailData = (id, setData) => {
  $.ajax({
    url: DETAIL_URL + "/" + id,
    datatype: 'json',
    success: function (data) {
      console.log(data);
      if (data) {
        setData(data)
        return
      } else {
        alert("에러가 발생했습니다.");
        return;
      }
    },
    error: function (request, status, error) {
      console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
      // ajax 처리가 결과가 에러이면 전송 여부는 false // 앞서 초기값을 false로 해 놓았지만 한번 더 선언을 한다.
    }
  });
}

function openDetailPopup() {
  deleteSelectedTypes()

  const id = this.parentNode.className
  console.log("id", id)
  // api에서 상세 데이터 받아서 input 만들기
  const data = getDetailData(this.parentNode.className, data => {
    popupName.value = data.name
    popupAddress.value = data.address
    popupLatitude.value = data.latitude
    popupLongitude.value = data.longitude
    popupReferences.value = data.references


    data.types?.map(type => {
      console.log("TYPE", type)
      makeSelectedTypes(type, type)
    })
  })

  console.log("TEST", data)
  popupStatus = 'edit'

  popupAreaModules[0].style.display = 'block'
  
  createPopupTitle.innerText = "정류장수정"
  popupCreateForm.action = EDIT_URL
  
  
  sendToHidden.value = id
}



//정류장등록
const createPopupInputs = document.querySelectorAll(".createPopup .popupArticleinput")
openPopup.addEventListener('click', openCreatePopup);

function openCreatePopup() {
  deleteSelectedTypes()

  popupAreaModules[0].style.display = 'block'
  popupName.value = ''
  popupAddress.value = ''
  popupLatitude.value = ''
  popupLongitude.value = ''
  popupReferences.value = ''
  
  createPopupTitle.innerText = "정류장등록"
  popupCreateForm.action = CREATE_URL
  
  // input value 비우기
}

createBtn.addEventListener('click', () => {
  for (i = 0; i < essential.length; i++) {
    if (essential[i].value == "") {
      return alert("입력하지 않은 필수 입력사항이 있습니다.")
    }
  };
  popupCreateForm.submit()
})

//삭제알림
deleteForm.addEventListener('submit', deleteData)

function deleteData(e) {
  e.preventDefault()
  
  const formData = new FormData(this);
  const id = formData.get('id')
  if (!id) {
    alert('삭제할 정류장을 선택해 주세요.')
  } else {
    if (confirm('정말로 삭제하시겠습니까?') == true) {
      this.submit()
    }
  }
}


window.onload = function () {
  addEventClosePopup()
  addEventSelectAllCheck()
}

const multipleSelect = document.querySelector("#multipleSelect")
const selectedTextDiv = document.querySelector(".selectedTextDiv")

multipleSelect.addEventListener('change', () => {
  const selectedItemInputs = document.querySelectorAll(".selectedItemInput")
  for (let i = 0; i < selectedItemInputs.length; i++) {
    if (selectedItemInputs[i].value == multipleSelect.options[multipleSelect.selectedIndex].value) {
      console.log("return")
      multipleSelect.selectedIndex = 0
      return;
    }
  }

  makeSelectedTypes(multipleSelect.options[multipleSelect.selectedIndex].textContent, multipleSelect.value)
  multipleSelect.selectedIndex = 0
})

const makeSelectedTypes = (text, value) => {
  const selectedItemDiv = document.createElement('div');
  selectedItemDiv.setAttribute("class", 'selectedItemDiv')

  const selectedItem = document.createElement('div');
  selectedItem.textContent = text
  selectedItemDiv.appendChild(selectedItem)

  const selectedItemInput = document.createElement('input');
  selectedItemInput.setAttribute("name", 'types')
  selectedItemInput.setAttribute("type", 'hidden')
  selectedItemInput.setAttribute("class", 'selectedItemInput')
  selectedItemInput.value = value
  selectedItemDiv.appendChild(selectedItemInput)

  const selectedItemDeleteBtn = document.createElement('div');
  selectedItemDeleteBtn.textContent = '삭제'
  selectedItemDeleteBtn.setAttribute('class', 'selectedItemDeleteBtn')

  selectedItemDeleteBtn.addEventListener("click", (e) => {
    e.target.parentNode.remove()
  })

  selectedItemDiv.appendChild(selectedItemDeleteBtn)
  selectedTextDiv.appendChild(selectedItemDiv)
}

const deleteSelectedTypes = () => {
  const typesLength = selectedTextDiv.childNodes.length
  for (let i = 0; i < typesLength; i++) {
    selectedTextDiv.childNodes[0].remove()
  }
}