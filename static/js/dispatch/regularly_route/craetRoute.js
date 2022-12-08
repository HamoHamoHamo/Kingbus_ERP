const crateRouteForm = document.querySelector(".routeinput")
const routeInputSave = document.querySelector(".routeInputSave")
const groupSelect = document.querySelector(".tdTypeC select[name=group]")
const driveDateCheck = document.querySelectorAll(".driveDateCheck")
const essential = document.querySelectorAll(".essential")
const inputPrice = document.querySelector(".inputPrice")
const inputDriverAllowance = document.querySelector(".inputDriverAllowance")
const referenceDateInput = document.querySelector(".referenceDateInput")

let savePrice0 = 0
let savePrice1 = 0

routeInputSave.addEventListener("click", saveCheck)

function saveCheck(){
    console.log(savePrice0);
    console.log(inputPrice.value.replace(/\,/g,""));
    for (i = 0; i < essential.length; i++){
        if(essential[i].value == ""){
            return alert("입력하지 않은 필수 입력사항이 있습니다.")
        }
    };
    let driveDateChecking = false
    for (i = 0; i < driveDateCheck.length; i++){
        if(driveDateCheck[i].checked){
            driveDateChecking = true
        }
    };
    if(groupSelect.options[groupSelect.selectedIndex].value == ""){
        alert("그룹을 선택해 주세요")
    }else if(!driveDateCheck){
        alert("운행요일을 선택해 주세요")
    }else if(savePrice0 !== inputPrice.value.replace(/\,/g,"") || savePrice1 !== inputDriverAllowance.value.replace(/\,/g,"") && referenceDateInput.value == ""){
        alert("금액/수당 수정 기준일을 선택해 주세요")
    }else{
        crateRouteForm.submit()
    }
}