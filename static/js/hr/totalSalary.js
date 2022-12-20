const salaryItem = document.querySelectorAll(".salaryList")
const totalSalaryList = document.querySelector(".totalSalaryList")

function totalSalary(){
    let price1 = 0
    let price2 = 0
    let price3 = 0
    let price4 = 0
    let price5 = 0
    let price6 = 0
    let price7 = 0
    let price8 = 0
    let price9 = 0
    let price10 = 0
    for (i = 0; i < salaryItem.length; i++){
        price1 = price1 + parseInt(salaryItem[i].children[5].children[0].value.replace(/\,/g,""))
        price2 = price2 + parseInt(salaryItem[i].children[6].children[0].value.replace(/\,/g,""))
        price3 = price3 + parseInt(salaryItem[i].children[7].children[0].value.replace(/\,/g,""))
        price4 = price4 + parseInt(salaryItem[i].children[8].innerText.replace(/\,/g,""))
        price5 = price5 + parseInt(salaryItem[i].children[9].innerText.replace(/\,/g,""))
        price6 = price6 + parseInt(salaryItem[i].children[10].innerText.replace(/\,/g,""))
        price7 = price7 + parseInt(salaryItem[i].children[11].innerText.replace(/\,/g,""))
        price8 = price8 + parseInt(salaryItem[i].children[12].innerText.replace(/\,/g,""))
        price9 = price9 + parseInt(salaryItem[i].children[13].innerText.replace(/\,/g,""))
        price10 = price10 + parseInt(salaryItem[i].children[14].innerText.replace(/\,/g,""))
    };
    totalSalaryList.children[1].innerText = price1.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    totalSalaryList.children[2].innerText = price2.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    totalSalaryList.children[3].innerText = price3.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    totalSalaryList.children[4].innerText = price4.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    totalSalaryList.children[5].innerText = price5.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    totalSalaryList.children[6].innerText = price6.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    totalSalaryList.children[7].innerText = price7.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    totalSalaryList.children[8].innerText = price8.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    totalSalaryList.children[9].innerText = price9.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    totalSalaryList.children[10].innerText = price10.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}

totalSalary()