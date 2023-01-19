const crateRouteForm = document.querySelector(".routeinput")
const routeInputSave = document.querySelector(".routeInputSave")
const groupSelect = document.querySelector(".tdTypeC select[name=group]")
const driveDateCheck = document.querySelectorAll(".driveDateCheck")
const essential = document.querySelectorAll(".essential")
const inputPrice = document.querySelector(".inputPrice")
const inputDriverAllowance = document.querySelector(".inputDriverAllowance")
const referenceDateInput = document.querySelector(".referenceDateInput")
const inputHidden = document.querySelector(".inputHidden")

const inputTime1 = document.querySelector("#departure_time1")
const inputTime2 = document.querySelector("#departure_time2")
const inputTime3 = document.querySelector("#arrival_time1")
const inputTime4 = document.querySelector("#arrival_time2")

let savePrice0 = 0
let savePrice1 = 0

routeInputSave.addEventListener("click", saveCheck)

function saveCheck(){
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
    let parms = new URLSearchParams(location.search)
    if(parms.has("id")){
        if(groupSelect.options[groupSelect.selectedIndex].value == ""){
            return alert("그룹을 선택해 주세요")
            
        }else if(!driveDateCheck){
            return alert("운행요일을 선택해 주세요")
            
        }else if((savePrice0 !== inputPrice.value.replace(/\,/g,"") || savePrice1 !== inputDriverAllowance.value.replace(/\,/g,"")) && referenceDateInput.value == ""){
            console.log("1", savePrice0, inputPrice.value.replace(/\,/g,""))
            console.log("2", savePrice1, inputDriverAllowance.value.replace(/\,/g,""))
            console.log("3", referenceDateInput.value)

            
            return alert("금액/수당 수정 기준일을 선택해 주세요")
        }else{
            // crateRouteForm.submit()
        }
    }else{
        if(groupSelect.options[groupSelect.selectedIndex].value == ""){
            return alert("그룹을 선택해 주세요")
        }else if(!driveDateCheck){
            return alert("운행요일을 선택해 주세요")
        }else{
            // crateRouteForm.submit()
        }
    }
    if (crateRouteForm.action == 'http://kingbuserp.link/dispatch/regularly/route/edit') {
        $.ajax({
            url: "/dispatch/regularly/route/edit/check",
            method: "POST",
            data: {
                "departure_date": `${inputTime1.value}:${inputTime2.value}`,
                "arrival_date": `${inputTime3.value}:${inputTime4.value}`,
                "id": inputHidden.value,
                'csrfmiddlewaretoken': csrftoken
            },
            datatype: 'json',
            success: function (data) {
                if (data['status'] == "fail") {
                    alert(`[${data.departure_date} ~ ${data.arrival_date}] \n${data.route} / ${data.bus}(${data.driver}) \n운행시간이 중복됩니다.`);
                    return;
                } else {
                    // alert(`${data.status}ss data${data.departure_date} ${data.arrival_date}`);
                    crateRouteForm.submit();
                }
            },
            error: function (request, status, error) {
                console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                // ajax 처리가 결과가 에러이면 전송 여부는 false // 앞서 초기값을 false로 해 놓았지만 한번 더 선언을 한다.
            },
        });
    } else {
        crateRouteForm.submit()
    }
}