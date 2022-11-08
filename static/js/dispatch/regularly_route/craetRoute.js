const crateRouteForm = document.querySelector(".routeinput")
const routeInputSave = document.querySelector(".routeInputSave")
const groupSelect = document.querySelector(".tdTypeB select[name=group]")

routeInputSave.addEventListener("click", saveCheck)

function saveCheck(){
    if(groupSelect.options[groupSelect.selectedIndex].value == ""){
        alert("그룹을 선택해 주세요")
    }else{
        crateRouteForm.submit()
    }
}