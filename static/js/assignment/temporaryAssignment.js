const inputTextPhoneNum = document.querySelector(".inputTextPhoneNum")
const inputTextTwice = document.querySelectorAll(".inputTextTwice")
const dispatchPaymen = document.querySelectorAll(".dispatchPaymen")
const needComma = document.querySelectorAll(".needComma")
const changeToVAT = document.querySelectorAll(".orderListItem .orderListSubContents:nth-child(16)")
const inputSave = document.querySelector(".inputSave")
const inputDispatchForm = document.querySelector(".inputDispatchForm")
const ListSub = document.querySelectorAll(".orderListSub .orderListItem")
const inputHidden = document.querySelector(".inputHidden")
const searchForm = document.querySelector(".searchForm")
const searchBtn = document.querySelector(".searchBtn")
const totalPrice1 = document.querySelector(".orderListTotal .orderListSubContents:nth-child(6)")

const essential = document.querySelectorAll(".essential")
const essentialSelect = document.querySelectorAll(".essentialSelect")


// 검색 날짜 역전 방지
searchBtn.addEventListener("click", orderPeriod)

function orderPeriod() {
    if (searchDate[0].value.replace(/\-/g, "") > searchDate[1].value.replace(/\-/g, "")) {
        alert("잘못된 범위입니다. 날짜를 다시 확인해 주세요.")
        searchDate[1].value = ""
    } else {
        searchForm.submit()
    }
}






// 운행시간 범위
for (i = 0; i < inputTextquarter.length; i++) {
    // inputTextquarter[i].addEventListener("change", orderDate)
}

function orderDate() {
    if (inputTextquarter[0].value !== "" && inputTextquarter[1].value !== "") {
        if (inputTextquarter[0].value.replace(/\-/g, "") > inputTextquarter[1].value.replace(/\-/g, "")) {
            alert("잘못된 범위입니다. 날짜를 다시 확인해 주세요.")
            inputTextquarter[1].value = ""
        }
    }
}


for (i = 0; i < inputTextTwice.length; i++) {
    inputTextTwice[i].addEventListener("change", orderTime)
}

function orderTime() {
    if (inputTextTwice[0].value > 23) {
        inputTextTwice[0].value = ""
    }
    if (inputTextTwice[2].value > 23) {
        inputTextTwice[2].value = ""
    }
    if (inputTextTwice[1].value > 59) {
        inputTextTwice[1].value = ""
    }
    if (inputTextTwice[3].value > 59) {
        inputTextTwice[3].value = ""
    }
    if (inputTextTwice[0].value !== "" && inputTextTwice[1].value !== "" && inputTextTwice[2].value !== "" && inputTextTwice[3].value !== "") {
        if (inputTextquarter[0].value == inputTextquarter[1].value) {
            if (inputTextTwice[0].value + inputTextTwice[1].value >= inputTextTwice[2].value + inputTextTwice[3].value) {
                alert("잘못된 범위입니다. 시간을 다시 확인해 주세요.")
                inputTextTwice[3].value = ""
            }
        }
    }
}

// 다음 항목으로 이동
inputTextTwice[0].addEventListener("input", nextFocus1)
inputTextTwice[2].addEventListener("input", nextFocus2)

function nextFocus1() {
    if (this.value.length === 2) {
        inputTextTwice[1].focus()
    }
}
function nextFocus2() {
    if (this.value.length === 2) {
        inputTextTwice[3].focus()
    }
}



// 금액 "," 추가/제거
inputTextPrice.addEventListener("click", removeComma)
inputTextPrice.addEventListener("change", addComma)
inputTextPrice.addEventListener("input", onlyNum)
inputTextDriverAllowance.addEventListener("click", removeComma)
inputTextDriverAllowance.addEventListener("change", addComma)
inputTextDriverAllowance.addEventListener("input", onlyNum)


function removeComma() {
    this.value = this.value.replace(/\,/g, "")
}

function addComma() {
    this.value = this.value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}

function onlyNum() {
    this.value = this.value.replace(/[^0-9]/g, '')
}

document.addEventListener("keydown", saveKeyPress)

function saveKeyPress(e) {
    if (e.keyCode === 113) {
        submitVaildation(e)
    }
}

inputSave.addEventListener("click", submitVaildation)

function submitVaildation(e) {
    e.preventDefault()
    for (i = 0; i < essential.length; i++){
        if(essential[i].value == ""){
            return alert("입력하지 않은 필수 입력사항이 있습니다.")
        }
    };   
    for (i = 0; i < essentialSelect.length; i++){
        if(essentialSelect[i].options[essentialSelect[i].selectedIndex].value == ""){
            return alert("입력하지 않은 필수 입력사항이 있습니다.")
        }
    };
    if (inputTextquarter[0].value.replace(/\-/g, "") > inputTextquarter[1].value.replace(/\-/g, "")) {
        alert("잘못된 범위입니다. 날짜를 다시 확인해 주세요.")
        inputTextquarter[1].value = ""
        return
    } else if (inputTextquarter[0].value == inputTextquarter[1].value) {
        if (inputTextTwice[0].value + inputTextTwice[1].value >= inputTextTwice[2].value + inputTextTwice[3].value) {
            alert("잘못된 범위입니다. 시간을 다시 확인해 주세요.")
            inputTextTwice[3].value = ""
        } else {
            if (inputTextPrice.value !== "" && inputTextPrice.value.length > 3) {
                inputTextPrice.value = inputTextPrice.value.replace(/\,/g, "")
            }
            if (inputTextDriverAllowance.value !== "" && inputTextDriverAllowance.value.length > 3) {
                inputTextDriverAllowance.value = inputTextDriverAllowance.value.replace(/\,/g, "")
            }
            // inputDispatchForm.submit()
        }
    } else {
        if (inputTextPrice.value !== "" && inputTextPrice.value.length > 3) {
            inputTextPrice.value = inputTextPrice.value.replace(/\,/g, "")
        }
        if (inputTextDriverAllowance.value !== "" && inputTextDriverAllowance.value.length > 3) {
            inputTextDriverAllowance.value = inputTextDriverAllowance.value.replace(/\,/g, "")
        }
        // inputDispatchForm.submit()
    }
    if (DETAIL_EXIST) {
        $.ajax({
            url: EDIT_CHECK_URL,
            method: "POST",
            data: {
                "departure_time": `${inputTextquarter[0].value} ${inputTextTwice[0].value}:${inputTextTwice[1].value}`,
                "arrival_time": `${inputTextquarter[1].value} ${inputTextTwice[2].value}:${inputTextTwice[3].value}`,
                "id": inputHidden.value,
                'csrfmiddlewaretoken': csrftoken,
                'current_page' : CURRENT_PAGE,
            },
            datatype: 'json',
            success: function (data) {
                if (data['status'] == "fail") {
                    alert(`[${data.departure_date} ~ ${data.arrival_date}] \n${data.route} / ${data.bus}(${data.driver}) \n운행시간이 중복됩니다.`);
                    return;
                } else {
                    // alert(`${data.status}ss data${data.departure_date} ${data.arrival_date}`);
                    inputDispatchForm.submit();
                }
            },
            error: function (request, status, error) {
                console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                // ajax 처리가 결과가 에러이면 전송 여부는 false // 앞서 초기값을 false로 해 놓았지만 한번 더 선언을 한다.
            },
        });
    } else {
        inputDispatchForm.submit()
    }

}

// 목록 "," 추가
function addCommaList() {
    for (i = 0; i < needComma.length; i++) {
        if (needComma[i].innerText.length > 3) {
            needComma[i].innerText = needComma[i].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        }
    }
}

