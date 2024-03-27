const salaryItem = document.querySelectorAll(".salaryList")
const totalSalaryList = document.querySelector(".totalSalaryList")

const salaryBase = document.querySelectorAll(".salaryBase")
const salaryServiceAllowance = document.querySelectorAll(".salaryServiceAllowance")
const salaryAnnualAllowance = document.querySelectorAll(".salaryAnnualAllowance")
const salaryPerformanceAllowance = document.querySelectorAll(".salaryPerformanceAllowance")
const salaryMeal = document.querySelectorAll(".salaryMeal")
const salaryAttendance = document.querySelectorAll(".salaryAttendance")
const salaryLeave = document.querySelectorAll(".salaryLeave")
const salaryOrder = document.querySelectorAll(".salaryOrder")
const salaryAssignment = document.querySelectorAll(".salaryAssignment")
const salaryAdditional = document.querySelectorAll(".salaryAdditional")
const salaryDeduction = document.querySelectorAll(".salaryDeduction")
const salaryTotal = document.querySelectorAll(".salaryTotal")
const salaryOvertimeAllowance = document.querySelectorAll(".salaryOvertimeAllowance")

const totalBase = document.querySelector(".totalBase")
const totalServiceAllowance = document.querySelector(".totalServiceAllowance")
const totalAnnualAllowance = document.querySelector(".totalAnnualAllowance")
const totalPerformanceAllowance = document.querySelector(".totalPerformanceAllowance")
const totalMeal = document.querySelector(".totalMeal")
const totalAttendance = document.querySelector(".totalAttendance")
const totalLeave = document.querySelector(".totalLeave")
const totalOrder = document.querySelector(".totalOrder")
const totalAssignment = document.querySelector(".totalAssignment")
const totalAdditional = document.querySelector(".totalAdditional")
const totalDeduction = document.querySelector(".totalDeduction")
const totalTotal = document.querySelector(".totalTotal")
const totalOvertimeAllowance = document.querySelector(".totalOvertimeAllowance")


function totalSalary(){
    let priceOvertimeAllowance = 0
    let priceBase = 0
    let priceServiceAllowance = 0
    let priceAnnualAllowance = 0
    let pricePerformanceAllowance = 0
    let priceMeal = 0
    let priceAttendance = 0
    let priceLeave = 0
    let priceOrder = 0
    let priceAssignment = 0
    let priceAdditional = 0
    let priceDeduction = 0
    let priceTotal = 0

    for (i = 0; i < salaryItem.length; i++){
        priceOvertimeAllowance = priceOvertimeAllowance + parseInt(salaryOvertimeAllowance[i]?.value.replace(/\,/g,""))
        priceBase = priceBase + parseInt(salaryBase[i]?.value.replace(/\,/g,""))
        priceServiceAllowance = priceServiceAllowance + parseInt(salaryServiceAllowance[i]?.value.replace(/\,/g,""))
        priceAnnualAllowance = priceAnnualAllowance + parseInt(salaryAnnualAllowance[i]?.value.replace(/\,/g,""))
        pricePerformanceAllowance = pricePerformanceAllowance + parseInt(salaryPerformanceAllowance[i]?.value.replace(/\,/g,""))
        priceMeal = priceMeal + parseInt(salaryMeal[i]?.value.replace(/\,/g,""))
        priceAttendance = priceAttendance + parseInt(salaryAttendance[i].innerText?.replace(/\,/g,""))
        priceLeave = priceLeave + parseInt(salaryLeave[i].innerText?.replace(/\,/g,""))
        priceOrder = priceOrder + parseInt(salaryOrder[i].innerText?.replace(/\,/g,""))
        priceAssignment = priceAssignment + parseInt(salaryAssignment[i].innerText?.replace(/\,/g,""))
        priceAdditional = priceAdditional + parseInt(salaryAdditional[i].innerText?.replace(/\,/g,""))
        priceDeduction = priceDeduction + parseInt(salaryDeduction[i].innerText?.replace(/\,/g,""))
        priceTotal = priceTotal + parseInt(salaryTotal[i].innerText?.replace(/\,/g,""))
    };
    totalOvertimeAllowance ? totalOvertimeAllowance.innerText = priceOvertimeAllowance?.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",") : null
    totalBase ? totalBase.innerText = priceBase.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",") : null;
    totalServiceAllowance ? totalServiceAllowance.innerText = priceServiceAllowance.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",") : null;
    totalAnnualAllowance ? totalAnnualAllowance.innerText = priceAnnualAllowance.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",") : null;
    totalPerformanceAllowance ? totalPerformanceAllowance.innerText = pricePerformanceAllowance.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",") : null;
    totalMeal ? totalMeal.innerText = priceMeal.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",") : null;
    totalAttendance ? totalAttendance.innerText = priceAttendance.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",") : null;
    totalLeave ? totalLeave.innerText = priceLeave.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",") : null;
    totalOrder ? totalOrder.innerText = priceOrder.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",") : null;
    totalAssignment ? totalAssignment.innerText = priceAssignment.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",") : null;
    totalAdditional ? totalAdditional.innerText = priceAdditional.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",") : null;
    totalDeduction ? totalDeduction.innerText = priceDeduction.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",") : null;
    totalTotal ? totalTotal.innerText = priceTotal.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",") : null;
}

totalSalary()