const groupCreateSave = document.querySelector(".groupCreateSave")
const time1 = document.querySelector(".routeTime input[name=departure_time1]")
const time2 = document.querySelector(".routeTime input[name=departure_time2]")
const time3 = document.querySelector(".routeTime input[name=arrival_time1]")
const time4 = document.querySelector(".routeTime input[name=arrival_time2]")
const routeId = document.querySelector(".routeinput input[name=id]")

groupCreateSave.addEventListener("click", editRoute)

function editRoute(e) {
    let parms = new URLSearchParams(location.search)
    if (parms.has("id")) {
        e.preventDefault()
        $.ajax({
            url: "/dispatch/regularly/route/edit/check",
            method: "POST",
            data: {
                "departure_time1": `${time1.value}`,
                "departure_time2": `${time2.value} `,
                "arrival_time1": `${time3.value} `,
                "arrival_time2": `${time4.value} `, 
                "id": `${routeId.value} `,
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
            }
        });
    }
}