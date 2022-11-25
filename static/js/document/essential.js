const uploadFileForm = document.querySelector(".uploadFileForm")
const uploadFileAdd = document.querySelector(".uploadFileAdd")
const essential = document.querySelector(".essential")
const documentFileInput = document.querySelector(".documentFileInput")
const groupAddBtn = document.querySelector(".groupAddBtn")
const groupAddpopupForm = document.querySelector(".groupAddpopupForm")
const groupEssential = document.querySelector(".groupEssential")

uploadFileAdd.addEventListener("click", createCheck)

function createCheck() {
    if (essential.value == "") {
        return alert("입력하지 않은 필수 입력사항이 있습니다.")
    }else if(documentFileInput.value == ""){
        return alert("입력하지 않은 필수 입력사항이 있습니다.")
    }
    uploadFileForm.submit()
}

groupAddBtn.addEventListener("click", createCheck)

function createCheck() {
    if (groupEssential.value == "") {
        return alert("입력하지 않은 필수 입력사항이 있습니다.")
    }
    groupAddpopupForm.submit()
}