const inputDelete = document.querySelector(".inputDelete")
const inputSave = document.querySelector(".inputSave")
const input = document.querySelector(".input")
const inputHidden = document.querySelector(".inputHidden")
const inputTime = document.querySelectorAll(".quarterBox .inputTextTwice")

inputDelete.addEventListener("click", deleteRoute)

function deleteRoute(e) {
    e.preventDefault()
    if (confirm("정말로 삭제하시겠습니까?")) {
        input.action = "/dispatch/regularly/route/delete"
        input.submit()
    }
}




inputSave.addEventListener("click", editRoute)

function editRoute(e) {
    if (window.location.search) {
        e.preventDefault()
        let edit = false;
        $.ajax({
            url: "/dispatch/regularly/route/edit/check",
            method: "POST",
            data: {
                "departure_time1": `${inputTime[0].value}`,
                "departure_time2": `${inputTime[1].value} `,
                "arrival_time1": `${inputTime[2].value} `,
                "arrival_time2": `${inputTime[3].value} `,
                "id": `${inputHidden.value} `,
                'csrfmiddlewaretoken': csrftoken
            },
            datatype: 'json',
            success: function (data) {
                if (data['status'] == "false") {
                    alert(`${data.week} ${data.route}[${data.departure_time}:${data.arrival_time}] - ${data.bus}(${data.driver}) \n운행시간이 중복됩니다.`);
                    return;
                } else {
                    
                    input.submit();
                }
            },
            error: function (request, status, error) {
                console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                // ajax 처리가 결과가 에러이면 전송 여부는 false // 앞서 초기값을 false로 해 놓았지만 한번 더 선언을 한다.
            },
            // complete: function () {
            //     if (edit){
            //         input.submit();
            //     }
                
            // }
        });
    }
}