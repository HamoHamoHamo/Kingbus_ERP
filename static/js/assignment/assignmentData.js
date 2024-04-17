const crateRouteForm = document.querySelector(".routeinput")
const routeInputSave = document.querySelector(".routeInputSave")
const inputGroup = document.querySelector(".inputGroup")
const essential = document.querySelectorAll(".essential")
const inputHidden = document.querySelector(".inputHidden")

const inputTime1 = document.querySelector("#start_time1")
const inputTime2 = document.querySelector("#start_time2")
const inputTime3 = document.querySelector("#end_time1")
const inputTime4 = document.querySelector("#end_time2")

const popupPriceList = document.querySelectorAll(".popupPrice")
let popupPriceChangeCheck = false

Array.from(popupPriceList).map(price => {
    price.addEventListener("change", () => popupPriceChangeCheck = true)
})


routeInputSave.addEventListener("click", saveCheck)

function saveCheck(){
    for (i = 0; i < essential.length; i++){
        if(essential[i].value == ""){
            return alert("입력하지 않은 필수 입력사항이 있습니다.")
        }
    };
    if(inputGroup.options[inputGroup.selectedIndex].value == ""){
        return alert("그룹을 선택해 주세요")
    }

    if (DETAIL_EXIST) {
        $.ajax({
            url: editCheckUrl,
            method: "POST",
            data: {
                "departure_time": `${inputTime1.value}:${inputTime2.value}`,
                "arrival_time": `${inputTime3.value}:${inputTime4.value}`,
                "id": inputHidden.value,
                'csrfmiddlewaretoken': csrftoken,
                'current_page' : CURRENT_PAGE
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