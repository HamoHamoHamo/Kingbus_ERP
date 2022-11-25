const btnModulesCreate = document.querySelector(".btnModulesCreate")
const creteForm = document.querySelector(".creteForm")
const essential = document.querySelectorAll(".essential")
const btnModulesEdit = document.querySelector(".btnModulesEdit")
const editForm = document.querySelector(".editForm")
const essentialEdit = document.querySelectorAll(".essentialEdit")

btnModulesCreate.addEventListener("click", createCheck)

function createCheck(){
    for (i = 0; i < essential.length; i++){
        if(essential[i].value == ""){
            return alert("입력하지 않은 필수 입력사항이 있습니다.")
        }
    };
    creteForm.submit()
}

btnModulesEdit.addEventListener("click", editCheck)

function editCheck(){
    for (i = 0; i < essentialEdit.length; i++){
        if(essentialEdit[i].value == ""){
            return alert("입력하지 않은 필수 입력사항이 있습니다.")
        }
    };
    editForm.submit()
}