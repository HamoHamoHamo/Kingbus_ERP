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
    const weekly_within_law_extension_wage = document.querySelector('.weekly_within_law_extension_wage')
    const weekly_outside_law_extension_wage = document.querySelector('.weekly_outside_law_extension_wage')
    const weekly_extension_additional_wage = document.querySelector('.weekly_extension_additional_wage')
    const night_shift_wage = document.querySelector('.night_shift_wage')
    const holiday_work_wage = document.querySelector('.holiday_work_wage')
    const additional_holiday_work_wage = document.querySelector('.additional_holiday_work_wage')
    const additional_holiday_work_wage_half = document.querySelector('.additional_holiday_work_wage_half')
    const annual_allowance = document.querySelector('.annual_allowance')
    const statutory_allowance = document.querySelector('.statutory_allowance')
    const sum_ordinary_salary_and_statutory_allowance = document.querySelector('.sum_ordinary_salary_and_statutory_allowance')

    const team_leader_allowance_roll_call = document.querySelector(".team_leader_allowance_roll_call")
    const team_leader_allowance_vehicle_management = document.querySelector(".team_leader_allowance_vehicle_management")
    const team_leader_allowance_task_management = document.querySelector(".team_leader_allowance_task_management")
    const full_attendance_allowance = document.querySelector(".full_attendance_allowance")
    const diligence_allowance = document.querySelector(".diligence_allowance")
    const accident_free_allowance = document.querySelector(".accident_free_allowance")
    const welfare_meal_allowance = document.querySelector(".welfare_meal_allowance")
    const welfare_fuel_allowance = document.querySelector(".welfare_fuel_allowance")
    const additional = document.querySelector(".additional")
    const deduction = document.querySelector(".deduction")
    const total = document.querySelector(".total")


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
    let total_weekly_within_law_extension_wage = 0
    let total_weekly_outside_law_extension_wage = 0
    let total_weekly_extension_additional_wage = 0
    let total_night_shift_wage = 0
    let total_holiday_work_wage = 0
    let total_additional_holiday_work_wage = 0
    let total_additional_holiday_work_wage_half = 0
    let total_annual_allowance = 0
    let total_statutory_allowance = 0
    let total_sum_ordinary_salary_and_statutory_allowance = 0

    let total_team_leader_allowance_roll_call = 0
    let total_team_leader_allowance_vehicle_management = 0
    let total_team_leader_allowance_task_management = 0
    let total_full_attendance_allowance = 0
    let total_diligence_allowance = 0
    let total_accident_free_allowance = 0
    let total_welfare_meal_allowance = 0
    let total_welfare_fuel_allowance = 0
    let total_additional = 0
    let total_deduction = 0
    let total_total = 0

    Object.entries(DATAS).map(([key, value]) => {
        total_total_work_minute += Number(value['total_work_minute'])
        total_hourly_wage += Number(removeComma(value['hourly_wage']))
        total_ordinary_hourly_wage += Number(removeComma(value['ordinary_hourly_wage']))
        total_wage += Number(removeComma(value['wage']))
        total_performance_allowance += Number(removeComma(value['performance_allowance']))
        total_meal += Number(removeComma(value['meal']))
        total_service_allowance += Number(removeComma(value['service_allowance']))
        total_ordinary_salary += Number(removeComma(value['ordinary_salary']))
        total_weekly_holiday_allowance += Number(removeComma(value['weekly_holiday_allowance']))
        total_legal_holiday_allowance += Number(removeComma(value['legal_holiday_allowance']))
        total_weekly_within_law_extension_wage += Number(removeComma(value['weekly_within_law_extension_wage']))
        total_weekly_outside_law_extension_wage += Number(removeComma(value['weekly_outside_law_extension_wage']))
        total_weekly_extension_additional_wage += Number(removeComma(value['weekly_extension_additional_wage']))
        total_night_shift_wage += Number(removeComma(value['night_shift_wage']))
        total_holiday_work_wage += Number(removeComma(value['holiday_work_wage']))
        total_additional_holiday_work_wage += Number(removeComma(value['additional_holiday_work_wage']))
        total_additional_holiday_work_wage_half += Number(removeComma(value['additional_holiday_work_wage_half']))
        total_annual_allowance += Number(removeComma(value['annual_allowance']))
        total_statutory_allowance += Number(removeComma(value['statutory_allowance']))
        total_sum_ordinary_salary_and_statutory_allowance += Number(removeComma(value['sum_ordinary_salary_and_statutory_allowance']))

        total_team_leader_allowance_roll_call += Number(removeComma(value['team_leader_allowance_roll_call']))
        total_team_leader_allowance_vehicle_management += Number(removeComma(value['team_leader_allowance_vehicle_management']))
        total_team_leader_allowance_task_management += Number(removeComma(value['team_leader_allowance_task_management']))
        total_full_attendance_allowance += Number(removeComma(value['full_attendance_allowance']))
        total_diligence_allowance += Number(removeComma(value['diligence_allowance']))
        total_accident_free_allowance += Number(removeComma(value['accident_free_allowance']))
        total_welfare_meal_allowance += Number(removeComma(value['welfare_meal_allowance']))
        total_welfare_fuel_allowance += Number(removeComma(value['welfare_fuel_allowance']))
        total_additional += Number(removeComma(value['additional']))
        total_deduction += Number(removeComma(value['deduction']))
        total_total += Number(removeComma(value['total']))
    })

    total_work_minute ? total_work_minute.innerText = `${parseInt(total_total_work_minute / 60)}시간 ${total_total_work_minute % 60}분` : null
    //hourly_wage ? total_hourly_wage.innerText = addcomma(total_hourly_wage.toString()) : null
    //ordinary_hourly_wage ? total_ordinary_hourly_wage.innerText = addcomma(total_ordinary_hourly_wage.toString()) : null
    wage ? wage.innerText = addComma(total_wage.toString()) : null
    performance_allowance ? performance_allowance.innerText = addComma(total_performance_allowance.toString()) : null
    meal ? meal.innerText = addComma(total_meal.toString()) : null
    service_allowance ? service_allowance.innerText = addComma(total_service_allowance.toString()) : null
    ordinary_salary ? ordinary_salary.innerText = addComma(total_ordinary_salary.toString()) : null
    weekly_holiday_allowance ? weekly_holiday_allowance.innerText = addComma(total_weekly_holiday_allowance.toString()) : null
    legal_holiday_allowance ? legal_holiday_allowance.innerText = addComma(total_legal_holiday_allowance.toString()) : null
    weekly_within_law_extension_wage ? weekly_within_law_extension_wage.innerText = addComma(total_weekly_within_law_extension_wage.toString()) : null
    weekly_outside_law_extension_wage ? weekly_outside_law_extension_wage.innerText = addComma(total_weekly_outside_law_extension_wage.toString()) : null
    weekly_extension_additional_wage ? weekly_extension_additional_wage.innerText = addComma(total_weekly_extension_additional_wage.toString()) : null
    night_shift_wage ? night_shift_wage.innerText = addComma(total_night_shift_wage.toString()) : null
    holiday_work_wage ? holiday_work_wage.innerText = addComma(total_holiday_work_wage.toString()) : null
    additional_holiday_work_wage ? additional_holiday_work_wage.innerText = addComma(total_additional_holiday_work_wage.toString()) : null
    additional_holiday_work_wage_half ? additional_holiday_work_wage_half.innerText = addComma(total_additional_holiday_work_wage_half.toString()) : null
    annual_allowance ? annual_allowance.innerText = addComma(total_annual_allowance.toString()) : null
    statutory_allowance ? statutory_allowance.innerText = addComma(total_statutory_allowance.toString()) : null
    sum_ordinary_salary_and_statutory_allowance ? sum_ordinary_salary_and_statutory_allowance.innerText = addComma(total_sum_ordinary_salary_and_statutory_allowance.toString()) : null
    
    team_leader_allowance_roll_call ? team_leader_allowance_roll_call.innerText = addComma(total_team_leader_allowance_roll_call.toString()) : null
    team_leader_allowance_vehicle_management ? team_leader_allowance_vehicle_management.innerText = addComma(total_team_leader_allowance_vehicle_management.toString()) : null
    team_leader_allowance_task_management ? team_leader_allowance_task_management.innerText = addComma(total_team_leader_allowance_task_management.toString()) : null
    full_attendance_allowance ? full_attendance_allowance.innerText = addComma(total_full_attendance_allowance.toString()) : null
    diligence_allowance ? diligence_allowance.innerText = addComma(total_diligence_allowance.toString()) : null
    accident_free_allowance ? accident_free_allowance.innerText = addComma(total_accident_free_allowance.toString()) : null
    welfare_meal_allowance ? welfare_meal_allowance.innerText = addComma(total_welfare_meal_allowance.toString()) : null
    welfare_fuel_allowance ? welfare_fuel_allowance.innerText = addComma(total_welfare_fuel_allowance.toString()) : null
    additional ? additional.innerText = addComma(total_additional.toString()) : null
    deduction ? deduction.innerText = addComma(total_deduction.toString()) : null
    total ? total.innerText = addComma(total_total.toString()) : null
}

function addComma(value) {
    return value?.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")
}

function removeComma(str) {
    // str이 문자열인지 확인
    if (typeof str === 'string') {
        return str.replace(/,/g, '');
    }
    // str이 null이거나 undefined일 경우 빈 문자열 반환
    return 0;
}