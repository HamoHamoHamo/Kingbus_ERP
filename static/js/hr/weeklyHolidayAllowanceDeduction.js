const weeklyDeduction = document.querySelectorAll(".weeklyDeductionTd")
const weeklyDeductionPopup = document.querySelector(".weeklyDeductionPopup")
const popupBgModulesWeeklyDeduction = document.querySelector(".popupBgModulesWeeklyDeduction")
const weeklyDeductionCloseBtn = document.querySelector(".weeklyDeductionCloseBtn")
const weeklyDeductionMoreHidden = document.querySelector(".weeklyDeductionMoreHidden")
const weeklyDeductionMoreHiddenMonth = document.querySelector(".weeklyDeductionMoreHiddenMonth")
const weeklyDeductionTableScroll = document.querySelector(".weeklyDeductionTableScroll tbody")
const weeklyDeductionListAllCheck = document.querySelector(".weeklyDeductionListAllCheck")
const weeklyDeductionDeleteBtn = document.querySelector(".weeklyDeductionDeleteBtn")
const weeklyDeductionDeleteForm = document.querySelector(".weeklyDeductionDeleteForm")


for (i = 0; i < weeklyDeduction.length; i++) {
    weeklyDeduction[i].addEventListener("click", openAddSalaryPopup)
};

function openAddSalaryPopup() {
    weeklyDeductionPopup.style.display = "block"
    weeklyDeductionMoreHidden.value = this.parentNode.children[0].children[0].value
    weeklyDeductionMoreHiddenMonth.value = searchMonth.value

    let targetItem = 0
    for (i = 0; i < addSalarly.length; i++) {
        if (addSalarly[i].parentNode === this.parentNode) {
            targetItem = i
        }
    };

    for (i = 0; i < weeklyDeductionList[targetItem].length; i++) {
        const addTr = document.createElement("tr")
        addTr.setAttribute("class", "table-list_body-tr weeklyDeductionList")
        weeklyDeductionTableScroll.appendChild(addTr)

        const addTd1 = document.createElement("td")
        addTd1.setAttribute("class", "table-list_body-tr_td")
        addTr.appendChild(addTd1)

        const addCheckbox = document.createElement("input")
        addCheckbox.setAttribute("type", "checkbox")
        addCheckbox.setAttribute("class", "weeklyDeductionChecker")
        addCheckbox.setAttribute("value", weeklyDeductionList[targetItem][i].id)
        addCheckbox.setAttribute("name", "id")
        addTd1.appendChild(addCheckbox)

        const addTd2 = document.createElement("td")
        addTd2.setAttribute("class", "table-list_body-tr_td priceTd")
        addTd2.innerText = weeklyDeductionList[targetItem][i].price
        addTr.appendChild(addTd2)

        const addTd3 = document.createElement("td")
        addTd3.setAttribute("class", "table-list_body-tr_td")
        addTd3.innerText = weeklyDeductionList[targetItem][i].remark
        addTr.appendChild(addTd3)
    };

    const price = document.querySelectorAll(".priceTd")
    const weeklyDeductionTrList = document.querySelectorAll(".weeklyDeductionList")
    const weeklyDeductionChecker = document.querySelectorAll(".weeklyDeductionChecker")
    weeklyDeductionTotal(price)
    weeklyDeductionChecking(weeklyDeductionTrList, weeklyDeductionChecker)

    weeklyDeductionDeleteBtn.addEventListener("click", weeklyDeductionDeleteAdd)

    function weeklyDeductionDeleteAdd() {
        for (i = 0; i < weeklyDeductionChecker.length; i++) {
            if (weeklyDeductionChecker[i].checked) {
                if (confirm('정말로 삭제하시겠습니까?')) {
                    return weeklyDeductionDeleteForm.submit()
                }
                else return;
            }
        };
        return alert("삭제할 항목을 선택해 주세요.")
    }

    weeklyDeductionListAllCheck.addEventListener("change", checkingAll)

    function checkingAll(){
        if(this.checked){
            for (i = 0; i < weeklyDeductionChecker.length; i++){
                weeklyDeductionChecker[i].checked = true
            };
        }else{
            for (i = 0; i < weeklyDeductionChecker.length; i++){
                weeklyDeductionChecker[i].checked = false
            };
        }
    }
}


popupBgModulesWeeklyDeduction.addEventListener("click", closeAddSalaryPopup)
weeklyDeductionCloseBtn.addEventListener("click", closeAddSalaryPopup)
SidemenuUseClose.addEventListener("click", closeAddSalaryPopup)

function closeAddSalaryPopup() {
    weeklyDeductionPopup.style.display = "none"
    weeklyDeductionTableScroll.innerText = ""
}


function weeklyDeductionTotal(price){
    let TotalAmount = 0
    for (i = 0; i < price.length; i++){
        TotalAmount = TotalAmount + parseInt(price[i].innerText)
        price[i].innerText = price[i].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    };
    totalAddSalaryPrice[2].innerText = TotalAmount
    totalAddSalaryPrice[2].innerText = totalAddSalaryPrice[2].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}



function weeklyDeductionChecking(weeklyDeductionTrList, weeklyDeductionChecker){

    for (i = 0; i < weeklyDeductionTrList.length; i++){
        weeklyDeductionTrList[i].addEventListener("click", checkingForList)
    };

    function checkingForList(){
        if(this.children[0].children[0].checked){
            this.children[0].children[0].checked = false
        }else{
            this.children[0].children[0].checked = true
        }
        
        let checker = 0
        for (i = 0; i < weeklyDeductionChecker.length; i++){
            if(weeklyDeductionChecker[i].checked){
                checker++
            }
        };
        if(weeklyDeductionChecker.length === checker){
            weeklyDeductionListAllCheck.checked = true
        }else{
            weeklyDeductionListAllCheck.checked = false
        }
    }
    



    for (i = 0; i < weeklyDeductionChecker.length; i++){
        weeklyDeductionChecker[i].addEventListener("click", checking)
    };
    
    function checking(e){
        e.stopPropagation()
        let checker = 0
        for (i = 0; i < weeklyDeductionChecker.length; i++){
            if(weeklyDeductionChecker[i].checked){
                checker++
            }
        };
        if(weeklyDeductionChecker.length === checker){
            weeklyDeductionListAllCheck.checked = true
        }else{
            weeklyDeductionListAllCheck.checked = false
        }
    }

}