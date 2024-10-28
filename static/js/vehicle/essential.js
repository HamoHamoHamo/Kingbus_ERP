const essential = document.querySelectorAll(".essential")
submitBtn.addEventListener("click", createCheck)
function createCheck(){
    for (i = 0; i < essential.length; i++){
        if(essential[i].value == ""){
            return alert("입력하지 않은 필수 입력사항이 있습니다.")
        }
    };
    vehicleForm.submit()
}

const maintenanceEssential = document.querySelectorAll(".maintenanceEssential")
const maintenanceCreateForm = document.querySelector(".maintenanceCreateForm")
const maintenanceSubmitBtn = document.querySelector(".maintenanceSubmitBtn")

maintenanceSubmitBtn.addEventListener("click", () => {
    for (i = 0; i < maintenanceEssential.length; i++){
        if(maintenanceEssential[i].value == ""){
            return alert("입력하지 않은 필수 입력사항이 있습니다.")
        }
    };
    maintenanceCreateForm.submit()
})

const photoEssential = document.querySelectorAll(".photoEssential")
const photoCreateForm = document.querySelector('.photoCreateForm')
const photoSubmitBtn = document.querySelector('.photoSubmitBtn')

photoSubmitBtn.addEventListener("click", () => {
    for (i = 0; i < photoEssential.length; i++){
        if(photoEssential[i].value == ""){
            return alert("입력하지 않은 필수 입력사항이 있습니다.")
        }
    };
    photoCreateForm.submit()
})