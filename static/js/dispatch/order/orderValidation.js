const inputTextPhoneNum = document.querySelector(".inputTextPhoneNum")
const inputTextPrice = document.querySelector(".inputTextPrice")
const inputTextDriverAllowance = document.querySelector(".inputTextDriverAllowance")
const inputTextTwice = document.querySelectorAll(".inputTextTwice")
const dispatchPrice = document.querySelectorAll(".dispatchPrice")
const dispatchPaymen = document.querySelectorAll(".dispatchPaymen")
const needComma1 = document.querySelectorAll(".orderListItem .orderListSubContents:nth-child(6)")
const needComma2 = document.querySelectorAll(".orderListItem .orderListSubContents:nth-child(7)")
const needComma3 = document.querySelectorAll(".orderListItem .orderListSubContents:nth-child(14)")
const needComma4 = document.querySelectorAll(".orderListItem .orderListSubContents:nth-child(15)")
const needComma5 = document.querySelectorAll(".orderListItem .orderListSubContents:nth-child(10)")
const changeToVAT = document.querySelectorAll(".orderListItem .orderListSubContents:nth-child(16)")
const inputSave = document.querySelector(".inputSave")
const inputDispatchForm = document.querySelector(".inputDispatchForm")
const ListSub = document.querySelectorAll(".orderListSub .orderListItem")
const inputHidden = document.querySelector(".inputHidden")
const searchForm = document.querySelector(".searchForm")
const searchBtn = document.querySelector(".searchBtn")
const totalPrice1 = document.querySelector(".orderListTotal .orderListSubContents:nth-child(6)")
const totalPrice2 = document.querySelector(".orderListTotal .orderListSubContents:nth-child(7)")
const totalPrice3 = document.querySelector(".orderListTotal .orderListSubContents:nth-child(14)")
const totalPrice4 = document.querySelector(".orderListTotal .orderListSubContents:nth-child(15)")


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




// 전화번호 "-" 추가
inputTextPhoneNum.addEventListener("input", phoneNumValidation)
inputTextPhoneNum.addEventListener("change", phoneNumValidationLength)

function phoneNumValidation() {
    inputTextPhoneNum.value = inputTextPhoneNum.value
        .replace(/[^0-9]/g, '')
        .replace(/^(\d{2,3})(\d{3,4})(\d{4})$/, `$1-$2-$3`);
}

function phoneNumValidationLength() {
    if (inputTextPhoneNum.value.length < 8) {
        alert("전화번호가 형식에 맞지 않습니다.")
        inputTextPhoneNum.value = ""
    }
}




// 금액 "," 추가/제거
inputTextPrice.addEventListener("click", removeComma)
inputTextPrice.addEventListener("change", addComma)
inputTextPrice.addEventListener("input", onlyNum)
inputTextDriverAllowance.addEventListener("click", removeComma)
inputTextDriverAllowance.addEventListener("change", addComma)
inputTextDriverAllowance.addEventListener("input", onlyNum)
for (i = 0; i < dispatchPrice.length; i++) {
    dispatchPrice[i].addEventListener("click", removeComma)
    dispatchPrice[i].addEventListener("change", addComma)
    dispatchPrice[i].addEventListener("input", onlyNum)
    dispatchPaymen[i].addEventListener("click", removeComma)
    dispatchPaymen[i].addEventListener("change", addComma)
    dispatchPaymen[i].addEventListener("input", onlyNum)
}


function removeComma() {
    this.value = this.value.replace(/\,/g, "")
}

function addComma() {
    this.value = this.value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}

function onlyNum() {
    this.value = this.value.replace(/[^0-9]/g, '')
}


inputSave.addEventListener("click", submitVaildation)

function submitVaildation(e) {
    e.preventDefault()
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
    if (inputDispatchForm.action == 'http://kingbuserp.link/dispatch/order/route/edit') {
        $.ajax({
            url: "/dispatch/order/route/edit/check",
            method: "POST",
            data: {
                "departure_date": `${inputTextquarter[0].value} ${inputTextTwice[0].value}:${inputTextTwice[1].value}`,
                "arrival_date": `${inputTextquarter[1].value} ${inputTextTwice[2].value}:${inputTextTwice[3].value}`,
                "id": inputHidden.value,
                'csrfmiddlewaretoken': csrftoken
            },
            datatype: 'json',
            success: function (data) {
                if (data['status'] == "fail") {
                    alert(`${data.route} ${data.driver} ${data.bus} \n운행시간이 중복됩니다.`);
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
    for (i = 0; i < needComma1.length; i++) {
        if (needComma1[i].innerText !== "" && needComma1[i].innerText > 3) {
            needComma1[i].innerText = needComma1[i].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        }
        if (needComma2[i].innerText !== "" && needComma2[i].innerText > 3) {
            needComma2[i].innerText = needComma2[i].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        }
        if (needComma3[i].innerText !== "" && needComma3[i].innerText > 3) {
            needComma3[i].innerText = needComma3[i].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        }
        if (needComma4[i].innerText !== "" && needComma4[i].innerText > 3) {
            needComma4[i].innerText = needComma4[i].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        }
        if (needComma5[i].innerText !== "") {
            needComma5[i].innerText = needComma5[i].innerText.replace(/\ /g, ", ");
        }
    }
}

// VAT 텍스트
function changeVAT() {
    for (i = 0; i < changeToVAT.length; i++) {
        if (changeToVAT[i].innerText == "n") {
            changeToVAT[i].innerText = "미포함"
        } else {
            changeToVAT[i].innerText = "포함"
        }
    }
}




// 합계 "," 추가
function addCommaTotal() {
    if (totalPrice1.innerText !== "" && totalPrice1.innerText > 3) {
        totalPrice1.innerText = totalPrice1.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    }
    if (totalPrice2.innerText !== "" && totalPrice2.innerText > 3) {
        totalPrice2.innerText = totalPrice2.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    }
    if (totalPrice3.innerText !== "" && totalPrice3.innerText > 3) {
        totalPrice3.innerText = totalPrice3.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    }
    if (totalPrice4.innerText !== "" && totalPrice4.innerText > 3) {
        totalPrice4.innerText = totalPrice4.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    }
}