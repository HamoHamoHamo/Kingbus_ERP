import { ClosePopup } from "/static/js/common/popupCommon.js"
import { Comma } from "/static/js/common/addComma.js"

window.onload = function () {
    ClosePopup.addClosePopupEvent();
    Comma.inputComma();
    // Comma.addCommaToInnerText();
    setTotal()
}


const hourlyRateEditPopup = document.querySelector("#hourlyRateEditPopup")
const hourlyRateEditPopupBtn = document.querySelector("#hourlyRateEditPopupBtn")



hourlyRateEditPopupBtn.addEventListener("click", () => {
    hourlyRateEditPopup.style.display = 'block'
})


const scrollYBox = document.querySelector(".orderListSubScroll")
const scrollBoxAll = document.querySelector(".orderListScrollYBox")
const scrollXBox = document.querySelector(".subScroll")

scrollYBox.addEventListener("scroll", moveScrollY)
scrollBoxAll.addEventListener("scroll", moveScrollY)

scrollXBox.addEventListener("scroll", moveScrollX)
scrollBoxAll.addEventListener("scroll", moveScrollX)

function moveScrollY(e) {
    // 세로 스크롤 동기화
    scrollYBox.scrollTop = e.target.scrollTop
    scrollBoxAll.scrollTop = e.target.scrollTop

}

function moveScrollX(e) {
    // 가로 스크롤 동기화
    scrollXBox.scrollLeft = e.target.scrollLeft
    scrollBoxAll.scrollLeft = e.target.scrollLeft
}

const hourlyWageForm = document.querySelector('.hourlyWageForm')

hourlyWageForm.addEventListener('submit', (e) => {
    e.preventDefault()
    const inputCommas = document.querySelectorAll('.inputComma')
    Array.from(inputCommas).forEach(item => {
        if (item.value == '') {
            window.alert("값을 입력해 주세요.")
        }
        item.value = item.value.replace(/\,/g, "");
    })
    e.target.submit()
})


// 아래 합계 표시
function setTotal() {

    const total_work_minute = document.querySelector('.total_work_minute')
    const hourly_wage = document.querySelector('.hourly_wage')
    const ordinary_hourly_wage = document.querySelector('.ordinary_hourly_wage')
    const wage = document.querySelector('.wage')
    const performance_allowance = document.querySelector('.performance_allowance')
    const meal = document.querySelector('.meal')
    const service_allowance = document.querySelector('.service_allowance')
    const ordinary_salary = document.querySelector('.ordinary_salary')
    const weekly_holiday_allowance = document.querySelector('.weekly_holiday_allowance')
    const legal_holiday_allowance = document.querySelector('.legal_holiday_allowance')
    const additional_wage = document.querySelector('.additional_wage')
    const night_shift_wage = document.querySelector('.night_shift_wage')
    const holiday_work_wage = document.querySelector('.holiday_work_wage')
    const additional_holiday_work_wage = document.querySelector('.additional_holiday_work_wage')
    const annual_allowance = document.querySelector('.annual_allowance')
    const statutory_allowance = document.querySelector('.statutory_allowance')
    const sum_ordinary_salary_and_statutory_allowance = document.querySelector('.sum_ordinary_salary_and_statutory_allowance')

    // console.log("SET", DATAS)
    let total_total_work_minute = 0
    let total_hourly_wage = 0
    let total_ordinary_hourly_wage = 0
    let total_wage = 0
    let total_performance_allowance = 0
    let total_meal = 0
    let total_service_allowance = 0
    let total_ordinary_salary = 0
    let total_weekly_holiday_allowance = 0
    let total_legal_holiday_allowance = 0
    let total_additional_wage = 0
    let total_night_shift_wage = 0
    let total_holiday_work_wage = 0
    let total_additional_holiday_work_wage = 0
    let total_annual_allowance = 0
    let total_statutory_allowance = 0
    let total_sum_ordinary_salary_and_statutory_allowance = 0


    Object.entries(DATAS).map(([key, value]) => {
        total_total_work_minute += Number(value['total_work_minute'])
        total_hourly_wage += Number(value['hourly_wage'])
        total_ordinary_hourly_wage += Number(value['ordinary_hourly_wage'])
        total_wage += Number(value['wage'])
        total_performance_allowance += Number(value['performance_allowance'])
        total_meal += Number(value['meal'])
        total_service_allowance += Number(value['service_allowance'])
        total_ordinary_salary += Number(value['ordinary_salary'])
        total_weekly_holiday_allowance += Number(value['weekly_holiday_allowance'])
        total_legal_holiday_allowance += Number(value['legal_holiday_allowance'])
        total_additional_wage += Number(value['additional_wage'])
        total_night_shift_wage += Number(value['night_shift_wage'])
        total_holiday_work_wage += Number(value['holiday_work_wage'])
        total_additional_holiday_work_wage += Number(value['additional_holiday_work_wage'])
        total_annual_allowance += Number(value['annual_allowance'])
        total_statutory_allowance += Number(value['statutory_allowance'])
        total_sum_ordinary_salary_and_statutory_allowance += Number(value['sum_ordinary_salary_and_statutory_allowance'])
    })

    total_work_minute.innerText = `${parseInt(total_total_work_minute / 60)}시간 ${total_total_work_minute % 60}분`
    hourly_wage.innerText = addComma(total_hourly_wage.toString())
    ordinary_hourly_wage.innerText = addComma(total_ordinary_hourly_wage.toString())
    wage.innerText = addComma(total_wage.toString())
    performance_allowance.innerText = addComma(total_performance_allowance.toString())
    meal.innerText = addComma(total_meal.toString())
    service_allowance.innerText = addComma(total_service_allowance.toString())
    ordinary_salary.innerText = addComma(total_ordinary_salary.toString())
    // weekly_holiday_allowance.innerText = addComma(total_weekly_holiday_allowance.toString())
    legal_holiday_allowance.innerText = addComma(total_legal_holiday_allowance.toString())
    additional_wage.innerText = addComma(total_additional_wage.toString())
    night_shift_wage.innerText = addComma(total_night_shift_wage.toString())
    holiday_work_wage.innerText = addComma(total_holiday_work_wage.toString())
    additional_holiday_work_wage.innerText = addComma(total_additional_holiday_work_wage.toString())
    annual_allowance.innerText = addComma(total_annual_allowance.toString())
    statutory_allowance.innerText = addComma(total_statutory_allowance.toString())
    sum_ordinary_salary_and_statutory_allowance.innerText = addComma(total_sum_ordinary_salary_and_statutory_allowance.toString())
}

function addComma(value) {
    return value?.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")
}