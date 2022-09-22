const inputTextPhoneNum = document.querySelector(".inputTextPhoneNum")
const inputTextPrice = document.querySelector(".inputTextPrice")
const inputTextDriverAllowance = document.querySelector(".inputTextDriverAllowance")
const inputTextTwice = document.querySelectorAll(".inputTextTwice")
const dispatchPrice = document.querySelector(".dispatchPrice")
const dispatchPaymen = document.querySelector(".dispatchPaymen")
const needComma1 = document.querySelectorAll(".listTableScroll .scrollListTable td:nth-child(3)")
const needComma2 = document.querySelectorAll(".listTableScroll .scrollListTable td:nth-child(4)")
const needComma3 = document.querySelectorAll(".listTableScroll .scrollListTable td:nth-child(8)")
const needComma4 = document.querySelectorAll(".listTableScroll .scrollListTable td:nth-child(9)")
const changeToVAT = document.querySelectorAll(".listTableScroll .scrollListTable td:nth-child(12)")
const inputSave = document.querySelector(".inputSave")
const inputDispatchForm = document.querySelector(".inputDispatchForm")
const ListSub = document.querySelectorAll(".orderListSub .orderListItem")


// 검색 날짜 역전 방지
for (i = 0; i < searchDate.length; i++) {
    searchDate[i].addEventListener("change", orderPeriod)
}

function orderPeriod() {
    if (searchDate[0].value.replace(/\-/g, "") > searchDate[1].value.replace(/\-/g, "")) {
        alert("잘못된 범위입니다. 날짜를 다시 확인해 주세요.")
        searchDate[1].value = ""
    }
}






// 운행시간 범위
for (i = 0; i < inputTextquarter.length; i++) {
    inputTextquarter[i].addEventListener("change", orderDate)
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
dispatchPrice.addEventListener("click", removeComma)
dispatchPrice.addEventListener("change", addComma)
dispatchPrice.addEventListener("input", onlyNum)
dispatchPaymen.addEventListener("click", removeComma)
dispatchPaymen.addEventListener("change", addComma)
dispatchPaymen.addEventListener("input", onlyNum)


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
            if (dispatchPrice.value !== "" && dispatchPrice.value.length > 3) {
                dispatchPrice.value = dispatchPrice.value.replace(/\,/g, "")
            }
            if (dispatchPaymen.value !== "" && dispatchPaymen.value.length > 3) {
                dispatchPaymen.value = dispatchPaymen.value.replace(/\,/g, "")
            }
            inputDispatchForm.submit()
        }
    } else {
        if (inputTextPrice.value !== "" && inputTextPrice.value.length > 3) {
            inputTextPrice.value = inputTextPrice.value.replace(/\,/g, "")
        }
        if (inputTextDriverAllowance.value !== "" && inputTextDriverAllowance.value.length > 3) {
            inputTextDriverAllowance.value = inputTextDriverAllowance.value.replace(/\,/g, "")
        }
        if (dispatchPrice.value !== "" && dispatchPrice.value.length > 3) {
            dispatchPrice.value = dispatchPrice.value.replace(/\,/g, "")
        }
        if (dispatchPaymen.value !== "" && dispatchPaymen.value.length > 3) {
            dispatchPaymen.value = dispatchPaymen.value.replace(/\,/g, "")
        }
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



// 콤마 추가
function pageLoadAddComma() {
    inputTextPrice.value = inputTextPrice.value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    inputTextDriverAllowance.value = inputTextDriverAllowance.value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    for (i = 0; i < ListSub.length; i++) {
        ListSub[i].children[2].innerText = ListSub[i].children[2].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        ListSub[i].children[3].innerText = ListSub[i].children[3].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        ListSub[i].children[8].innerText = ListSub[i].children[8].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        ListSub[i].children[9].innerText = `${ListSub[i].children[3].innerText.replace(/\,/g, "") - ListSub[i].children[8].innerText.replace(/\,/g, "")}`
        ListSub[i].children[9].innerText = ListSub[i].children[9].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        if (ListSub[i].children[12].innerText == "y") {
            ListSub[i].children[12].innerText = "VAT 포함"
        }else{
            ListSub[i].children[12].innerText = "VAT 미포함"
        }
    }
}