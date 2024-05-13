import { addEventClosePopup, closePopup } from "/static/js/common/popupCommon.js"

const popupAreaModules = document.querySelectorAll('.popupAreaModules')
const groupAddBtn = document.querySelector('.groupAddBtn')
const businessGroupEditBtn = document.querySelectorAll(".businessGroupEditBtn")
const businessPopupGroupId = document.querySelectorAll(".businessPopupGroupId")
const businessPopupCloseBtn = document.querySelector('.businessPopupCloseBtn')

businessPopupCloseBtn.addEventListener("click", closePopup)
groupAddBtn.addEventListener("click", openBusinessPopup)

for(i=0; i<businessGroupEditBtn.length; i++) {
    businessGroupEditBtn[i].addEventListener("click", openBusinessEditPopup)
}

addEventClosePopup()

function initPopupInput() {
    popupInputId.value = ''
    popupInputNumber.value = ''
    popupInputName.value = ''
    for (let i=0; i<businessPopupGroupId.length; i++) {
        businessPopupGroupId[i].checked = false
    }
}

function openBusinessPopup() {
    initPopupInput()
    popupAreaModules[0].style.display = 'block';
}

function openBusinessEditPopup() {
    const popupInputId = document.querySelector('#popupInputId')
    const popupInputNumber = document.querySelector('#popupInputNumber')
    const popupInputName = document.querySelector('#popupInputName')

    openBusinessPopup()

    const id = this.previousElementSibling.classList[0]
    const groupData = businessGroupData[id]

    popupInputId.value = id
    popupInputNumber.value = businessData[id]['number']
    popupInputName.value = businessData[id]['name']

    for (let i=0; i<businessPopupGroupId.length; i++) {
        let checkbox = businessPopupGroupId[i]
        for (let j=0; j<groupData.length; j++) {
            if (groupData[j]['id'] == checkbox.value) {
                checkbox.checked = true
            }
        }
    }
}