const vehicleCreateForm = document.querySelector(".vehicleCreateForm")
const essential = document.querySelectorAll(".essential")
const vehicleEditForm = document.querySelector(".vehicleEditForm")
const essentialEdit = document.querySelectorAll(".essentialEdit")

createBtn[0].addEventListener("click", createCheck)

function createCheck(){
    for (i = 0; i < essential.length; i++){
        if(essential[i].value == ""){
            return alert("입력하지 않은 필수 입력사항이 있습니다.")
        }
    };
    if(BusLicenseFileInput.value == ""){
        return alert("입력하지 않은 필수 입력사항이 있습니다.")
    }    
    vehicleCreateForm.submit()
}

createBtn[1].addEventListener("click", editCheck)

function editCheck(){
    for (i = 0; i < essentialEdit.length; i++){
        if(essentialEdit[i].value == ""){
            return alert("입력하지 않은 필수 입력사항이 있습니다.")
        }
    };
    if(BusLicenseFileTextEdit.value == ""){
        return alert("입력하지 않은 필수 입력사항이 있습니다.")
    }
    vehicleEditForm.submit()
}