const clientCreteForm = document.querySelector(".clientCreteForm")
const clientCreateBtn = document.querySelector(".clientCreateBtn")
const essential = document.querySelectorAll(".essential")
const clientEditForm = document.querySelector(".clientEditForm")
const clientSaveEditBtn = document.querySelector(".clientSaveEditBtn")
const editEssential = document.querySelectorAll(".editEssential")

clientCreateBtn.addEventListener("click", createEssential)

function createEssential(){
    for (i = 0; i < essential.length; i++){
        if(essential[i].value == ""){
            return alert("입력하지 않은 필수 입력사항이 있습니다.")
        }
    };
    clientCreteForm.submit()
}

clientSaveEditBtn.addEventListener("click", editEssentialForm)

function editEssentialForm(){
    for (i = 0; i < editEssential.length; i++){
        if(editEssential[i].value == ""){
            return alert("입력하지 않은 필수 입력사항이 있습니다.")
        }
    };
    clientEditForm.submit()
}