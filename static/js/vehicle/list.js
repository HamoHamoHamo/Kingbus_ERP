const openCrete = document.querySelector(".addVehicle")
const uploadExcelBtn = document.querySelector(".uploadExcel")
const popupAreaModules = document.querySelectorAll(".popupAreaModules")
const popupBgModules = document.querySelectorAll(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const PopupCloseBtn = document.querySelectorAll(".closeBtn")
const openDetail = document.querySelectorAll(".openDetail")
const saveBtn = document.querySelector(".saveBtn")
const checkBox = document.querySelectorAll(".tableBody input")
const vehicleListForm = document.querySelector(".vehicleListForm")


// 차량수정 팝업 input
const vehicleNum1 = document.querySelector(".vehicleNum1")
const vehicleNum2 = document.querySelector(".vehicleNum2")
const driver_name = document.querySelector(".driver_name")
const maker = document.querySelector(".maker")
const vehicle_type = document.querySelector(".vehicle_type")
const vehicle_id = document.querySelector(".vehicle_id")
const model_year = document.querySelector(".model_year")
const release_date = document.querySelector(".release_date")
const passenger_num = document.querySelector(".passenger_num")
const motor_type = document.querySelector(".motor_type")
const rated_output = document.querySelector(".rated_output")
const type = document.querySelector(".type")
const check_date = document.querySelector(".check_date")
const garage = document.querySelector(".garage")

const vehicle_price = document.querySelector(".vehicle_price")
const number_price = document.querySelector(".number_price")
const insurance_pay_date = document.querySelector(".insurance_pay_date")
const insurance_price = document.querySelector(".insurance_price")
const monthly_installment = document.querySelector(".monthly_installment")
const remaining_installment_amount = document.querySelector(".remaining_installment_amount")
const depreciation_month = document.querySelector(".depreciation_month")
const depreciation_year = document.querySelector(".depreciation_year")

const ableBusEdit = document.querySelector("#ableBusEdit")
const disableBusEdit = document.querySelector("#disableBusEdit")
// 차량옵션
const ledTrue = document.querySelector("#ledTrue")
const ledFalse = document.querySelector("#ledFalse")
const fridgeTrue = document.querySelector("#fridgeTrue")
const fridgeFalse = document.querySelector("#fridgeFalse")
const singTrue = document.querySelector("#singTrue")
const singFalse = document.querySelector("#singFalse")
const usbTrue = document.querySelector("#usbTrue")
const usbFalse = document.querySelector("#usbFalse")
const waterHeaterTrue = document.querySelector("#waterHeaterTrue")
const waterHeaterFalse = document.querySelector("#waterHeaterFalse")
const tvTrue = document.querySelector("#tvTrue")
const tvFalse = document.querySelector("#tvFalse")

const remark = document.querySelector("#remark")


const sendToHidden = document.querySelector(".sendToHidden")
const fileDeleteBtn = document.querySelectorAll(".fileDeleteBtn")
const BusLicenseFileText = document.querySelector(".BusLicenseFileText")
const BusLicenseFileInput = document.querySelector(".BusLicenseFileInput")
const BusLicenseFileInputEdit = document.querySelector(".BusLicenseFileInputEdit")
const addUnit1 = document.querySelectorAll(".tableBody td:nth-child(7)")
const addUnit2 = document.querySelectorAll(".tableBody td:nth-child(9)")
const PopupDatainput = document.querySelectorAll(".PopupDataInput")
const deleteBusEdit = document.querySelector("#deleteBusEdit")

const submitBtn = document.querySelector(".submitBtn")
const vehicleForm = document.querySelector(".vehicleForm")


//등록팝업 열기
openCrete.addEventListener("click", openCreatePopup)

function openCreatePopup() {
    popupAreaModules[0].style.display = "block"
    submitBtn.innerText = "등록"
    vehicleForm.action = VEHICLE_CREATE_URL

    vehicleNum1.value = ''
    vehicleNum2.value = ''
    driver_name.value = ''
    maker.value = ''
    vehicle_type.value = ''
    passenger_num.value = ''
    type.value = ''
    model_year.value = ''
    vehicle_id.value = ''
    release_date.value = ''
    motor_type.value = ''
    rated_output.value = ''
    check_date.value = ''
    garage.value = ''
    ableBusEdit.checked = true
    
    // 차량금액정보
    vehicle_price.value = ''
    number_price.value = ''
    insurance_pay_date.value = ''
    insurance_price.value = ''
    monthly_installment.value = ''
    remaining_installment_amount.value = ''
    depreciation_month.value = ''
    depreciation_year.value = ''
    
    remark.innerText = ''
    
    
    ledFalse.checked = true
    fridgeFalse.checked = true
    singFalse.checked = true
    usbFalse.checked = true
    waterHeaterFalse.checked = true
    tvFalse.checked = true
    
    sendToHidden.value = ''
    
}


uploadExcelBtn.addEventListener("click", openUploadExcelPopup)

function openUploadExcelPopup() {
    popupAreaModules[1].style.display = "block"
}



//팝업닫기
Array.from(popupBgModules).forEach(item => item.addEventListener("click", closePopup))
Array.from(PopupCloseBtn).forEach(item => item.addEventListener("click", closePopup))

SidemenuUseClose.addEventListener("click", closePopup)

function closePopup() {
    for (i = 0; i < popupAreaModules.length; i++) {
        popupAreaModules[i].style.display = "none"
    }
}



//상세팝업 열기
for (i = 0; i < openDetail.length; i++) {
    openDetail[i].addEventListener("click", openDetailPopup)
}

function openDetailPopup() {
    console.log("this.className", this.classList)
    popupAreaModules[0].style.display = "block"
    const index = this.classList[0]

    submitBtn.innerText = "저장"
    vehicleForm.action = VEHICLE_EDIT_URL

    // 차량정보
    sendToHidden.value = this.parentNode.classList[0];

    vehicleNum1.value = vehicleDatas[index].vehicle_num0
    vehicleNum2.value = vehicleDatas[index].vehicle_num
    driver_name.value = vehicleDatas[index].driver
    
    if (vehicleDatas[index].use == "미사용") {
        disableBusEdit.checked = true
    } else {
        ableBusEdit.checked = true
    }
    maker.value = vehicleDatas[index].maker
    vehicle_type.value = vehicleDatas[index].vehicle_type
    passenger_num.value = vehicleDatas[index].passenger_num
    type.value = vehicleDatas[index].type
    model_year.value = vehicleDatas[index].model_year
    vehicle_id.value = vehicleDatas[index].vehicle_id
    release_date.value = vehicleDatas[index].release_date
    motor_type.value = vehicleDatas[index].motor_type
    rated_output.value = vehicleDatas[index].rated_output
    check_date.value = vehicleDatas[index].check_date
    garage.value = vehicleDatas[index].garage
    

    // 차량금액정보
    vehicle_price.value = vehicleDatas[index].vehicle_price
    number_price.value = vehicleDatas[index].number_price
    insurance_pay_date.value = vehicleDatas[index].insurance_pay_date
    insurance_price.value = vehicleDatas[index].insurance_price
    monthly_installment.value = vehicleDatas[index].monthly_installment
    remaining_installment_amount.value = vehicleDatas[index].remaining_installment_amount
    depreciation_month.value = vehicleDatas[index].depreciation_month
    depreciation_year.value = vehicleDatas[index].depreciation_year

    remark.innerText = vehicleDatas[index].remark
    // 차량옵션
    if (vehicleDatas[index].led == "False") {
        ledFalse.checked = true
    } else {
        ledTrue.checked = true
    }
    
    if (vehicleDatas[index].fridge == "False") {
        fridgeFalse.checked = true
    } else {
        fridgeTrue.checked = true
    }

    if (vehicleDatas[index].sing == "False") {
        singFalse.checked = true
    } else {
        singTrue.checked = true
    }

    if (vehicleDatas[index].usb == "False") {
        usbFalse.checked = true
    } else {
        usbTrue.checked = true
    }

    if (vehicleDatas[index].water_heater == "False") {
        waterHeaterFalse.checked = true
    } else {
        waterHeaterTrue.checked = true
    }

    if (vehicleDatas[index].tv == "False") {
        tvFalse.checked = true
    } else {
        tvTrue.checked = true
    }

}



//삭제알림
let checkCounte = false;

for (i = 0; i < checkBox.length; i++) {
    checkBox[i].addEventListener('change', checking)
}

function checking() {
    checkCounte = false
    for (i = 0; i < checkBox.length; i++) {
        if (checkBox[i].checked) {
            checkCounte = true
        }
        console.log(checkBox[i].checked)
    }
}


vehicleListForm.addEventListener('submit', deleteData)

function deleteData(e) {
    if (!checkCounte) {
        e.preventDefault()
        alert('삭제할 차량을 선택해 주세요.')
    } else {
        if (confirm('정말로 삭제하시겠습니까?') == false) {
            e.preventDefault()
        }
    }
}


//파일명 변경
// BusLicenseFileInput.addEventListener("change", changeFileBusLicense)
// BusLicenseFileInputEdit.addEventListener("change", changeFileLicenseEdit)

function changeFileBusLicense() {
    BusLicenseFileText.value = BusLicenseFileInput.files[0].name
}
function changeFileLicenseEdit() {
    console.log("A")
    BusLicenseFileTextEdit.value = BusLicenseFileInputEdit.files[0].name
}



// 파일삭제
fileDeleteBtn[0].addEventListener("click", deleteFileBusLicense)

function deleteFileBusLicense() {
    BusLicenseFileText.value = ""
    BusLicenseFileInput.value = ""
}
function deleteFileLicensEdit() {
    BusLicenseFileTextEdit.value = ""
    BusLicenseFileInputEdit.value = ""
}




// , 추가, 단위추가
window.onload = function () {
    for (i = 0; i < addUnit1.length; i++) {
        if (addUnit1[i].innerText !== "") {
            addUnit1[i].innerText = `${addUnit1[i].innerText}명`
        }
        if (addUnit2[i].innerText !== "") {
            addUnit2[i].innerText = `${addUnit2[i].innerText}년`
        }
    }
}

//차량번호, 연식
// PopupDataInput[1].addEventListener('change', busNumChecker)
// PopupDataInput[7].addEventListener('change', yearChecker)

// function busNumChecker(){
//   if(this.value.length >= 5){
//     this.value = this.value.substr(0,5)
//   }else if(this.value.length <= 3){
//     alert("4자리의 숫자를 입력해 주세요.")
//   }
// }
// function yearChecker(){
//   if(this.value.length >= 5){
//     this.value = this.value.substr(0,4)
//   }else if(this.value.length <= 3){
//     alert("4자리의 숫자를 입력해 주세요.")
//   }
// else if(this.value.substr(2,) !== 19 && this.value.substr(2,) !== 20){
//   alert("올바른 연도를 입력해 주세요")
//   this.value = ""
// }
// }