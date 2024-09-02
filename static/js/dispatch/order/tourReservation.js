const tourReservationBtn = document.querySelector(".tourReservationBtn")
const tourReservationCloseBtn = document.querySelector(".tourReservationCloseBtn")
const payDatetime = document.querySelectorAll(".payDatetime")
const paymentStatus = document.querySelectorAll(".paymentStatus")
const tourReservationAddBtn = document.querySelector(".tourReservationAddBtn")
const saveBtn = document.querySelector(".save")
const deleteBtn = document.querySelector(".delete")
const tourReservationCustomerForm = document.querySelector(".tourReservationCustomerForm")
const reservationCustomerCount = document.querySelector(".reservationCustomerCount")
const tourReservationInfoSaveBtn = document.querySelector(".tourReservationInfoSaveBtn")
const reservationInfoForm = document.querySelector("#reservationInfoForm")

// 여행상품 정보 저장
tourReservationInfoSaveBtn.addEventListener("click", () => {
    reservationInfoForm.submit()
})

// 예약자 명단 저장
saveBtn.addEventListener("click", () => {
    tourReservationCustomerForm.action = TOUR_CUSTOMER_SAVE_URL
    tourReservationCustomerForm.submit()
})

// 예약자 명단 삭제
deleteBtn.addEventListener("click", () => {
    tourReservationCustomerForm.action = TOUR_CUSTOMER_DELETE_URL
    if (confirm("정말로 삭제하시겠습니까?")){
        tourReservationCustomerForm.submit()
    }
})


tourReservationBtn.addEventListener("click", openTourReservationPopup)

function openTourReservationPopup() {
    popupAreaModules[6].style.display = "block"
}

popupBgModules[6].addEventListener("click", closeTourReservationPopup)
SidemenuUseClose.addEventListener("click", closeTourReservationPopup)
tourReservationCloseBtn.addEventListener("click", closeTourReservationPopup)

function closeTourReservationPopup() {
    popupAreaModules[6].style.display = "none"
}

tourReservationAddBtn.addEventListener("click", addTourReservationCustomer)

console.log(reservationCustomerCount.innerText.split("/")[1])
function addTourReservationCustomer() {
    // 최대 예약자 수 넘는지 확인
    const currentCount = parseInt(reservationCustomerCount?.innerText.split("/")[0])
    const maxCount = parseInt(reservationCustomerCount?.innerText.split("/")[1])
    if (currentCount >= maxCount) {
        alert("최대 예약 인원에 도달했습니다.")
        return
    }

    const reservationCustomerName = document.querySelector("#reservationCustomerName")
    const reservationCustomerPhone = document.querySelector("#reservationCustomerPhone")
    const reservationCustomerBank = document.querySelector("#reservationCustomerBank")
    const reservationTbody = document.querySelector("#reservationTbody")

    // 예약자명 입력 확인
    if (!(reservationCustomerName.value) ||
        !(reservationCustomerPhone.value) ||
        !(reservationCustomerBank.value) ) {
        window.alert("예약자 정보를 입력해 주세요")
        return 
    }

    const checkTd = createTourReservationCustomerTd()
    const checkbox = document.createElement("input")
    checkbox.setAttribute("type", "checkbox")
    checkTd.appendChild(checkbox)

    const nameTd = createTourReservationCustomerTd()
    nameTd.textContent = reservationCustomerName.value
    const nameInput = createTourReservationCustomerInput("name", reservationCustomerName.value)

    const phoneTd = createTourReservationCustomerTd()
    phoneTd.textContent = reservationCustomerPhone.value
    const phoneInput = createTourReservationCustomerInput("phone", reservationCustomerPhone.value)

    const bankTd = createTourReservationCustomerTd()
    bankTd.textContent = reservationCustomerBank.value
    const bankInput = createTourReservationCustomerInput("bank", reservationCustomerBank.value)

    const payDatetimeTd = createTourReservationCustomerTd()
    const datetimeInput = document.createElement("input")
    datetimeInput.setAttribute("type", "datetime-local")
    datetimeInput.setAttribute("name", "new_pay_datetime")
    payDatetimeTd.appendChild(datetimeInput)

    const paymentStatusTd = createTourReservationCustomerTd()
    const statusSelect = document.createElement("select")
    statusSelect.setAttribute("name", "new_payment_status")

    const statusSelectOption1 = document.createElement("option")
    statusSelectOption1.setAttribute("value", "결제대기")
    statusSelectOption1.textContent = "결제대기"
    const statusSelectOption2 = document.createElement("option")
    statusSelectOption2.setAttribute("value", "결제완료")
    statusSelectOption2.textContent = "결제완료"
    statusSelect.appendChild(statusSelectOption1)
    statusSelect.appendChild(statusSelectOption2)
    paymentStatusTd.appendChild(statusSelect)

    const tr = document.createElement("tr")
    tr.setAttribute("class", "table-list_body-tr")
    tr.appendChild(checkTd)
    tr.appendChild(nameTd)
    tr.appendChild(phoneTd)
    tr.appendChild(bankTd)
    tr.appendChild(payDatetimeTd)
    tr.appendChild(paymentStatusTd)
    tr.appendChild(nameInput)
    tr.appendChild(phoneInput)
    tr.appendChild(bankInput)
    
    reservationTbody.appendChild(tr)

    // 초기화
    reservationCustomerName.value = ""
    reservationCustomerPhone.value = ""
    reservationCustomerBank.value = ""

    reservationCustomerCount.innerText = `${currentCount + 1}/${maxCount}`
}

function createTourReservationCustomerTd() {
    const td = document.createElement("td")
    td.setAttribute("class", "table-list_body-tr_td")
    return td
}

function createTourReservationCustomerInput(name, value) {
    const input = document.createElement("input")
    input.setAttribute("type", "hidden")
    input.setAttribute("name", name)
    input.value = value
    return input
}


Array.from(paymentStatus).forEach(item => {
    item.addEventListener("change", setReservationCustomerId)
})

Array.from(payDatetime).forEach(item => {
    item.addEventListener("change", setReservationCustomerId)
})

function setReservationCustomerId(e) {
    const parentTr = e.target.parentNode.parentNode
    if (!(parentTr.querySelector("input[name=edit_customer]"))) {
        const editCustomer = document.createElement("input")
        editCustomer.setAttribute("type", "hidden")
        editCustomer.setAttribute("name", "edit_customer")
        editCustomer.setAttribute("value", parentTr.children[0].children[0].value)
        parentTr.appendChild(editCustomer)
        parentTr.querySelector(".payDatetime")?.setAttribute("name", "pay_datetime")
        parentTr.querySelector(".paymentStatus")?.setAttribute("name", "payment_status")
    }
}