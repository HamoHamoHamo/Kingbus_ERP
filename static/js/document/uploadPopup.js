
const popupAreaModules = document.querySelectorAll('.popupAreaModules');
const popupBgModules = document.querySelectorAll(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const closeBtn = document.querySelectorAll(".popupFooter div")
const upload = document.querySelectorAll(".uploadFile")
const FileInput = document.querySelector(".documentFileInput")
const FileText = document.querySelector(".documentFileText")
const fileDeleteBtn = document.querySelector(".fileDeleteBtn")
const popupArticleInput = document.querySelectorAll(".popupArticleInput")
const addGroupBox = document.querySelector(".addGroupBox")
const hiddenGroupId = document.querySelector(".hiddenGroupId")



// 업로드 팝업 열기
for (i = 0; i < upload.length; i++) {
    upload[i].addEventListener("click", uploadOpen)
}

function uploadOpen() {
    popupAreaModules[0].style.display = 'block'
    hiddenGroupId.value = this.parentNode.parentNode.parentNode.parentNode.children[0].children[0].children[0].children[0].classList[1].split("group")[1]
}





// 그룹추가 팝업 열기
addGroupBox.addEventListener("click", addGroupOpen)

function addGroupOpen() {
    popupAreaModules[1].style.display = 'block'
}





//팝업닫기
for (i = 0; i < popupBgModules.length; i++) {
    popupBgModules[i].addEventListener("click", closePopup)
    // popupCloseBtn[i].addEventListener("click", closePopup)
}

SidemenuUseClose.addEventListener("click", closePopup)

closeBtn[0].addEventListener("click", closePopup)
closeBtn[1].addEventListener("click", closePopup)

function closePopup() {
    popupAreaModules[0].style.display = "none"
    popupAreaModules[1].style.display = "none"
    removeData()
}

function removeData() {
    popupArticleInput[0].value = ""
    popupArticleInput[1].value = ""
    FileText.value = ""
}





//파일명 변경
FileInput.addEventListener("change", changeFile)

function changeFile() {
    popupArticleInput[0].value = FileInput.files[0].name
    FileText.value = FileInput.files[0].name
}




// 파일삭제
fileDeleteBtn.addEventListener("click", deleteFile)

function deleteFile() {
    FileText.value = ""
    FileInput.value = ""
}
