const deduction = document.querySelectorAll(".scrolling_table-list_body td:nth-child(11)")
const deductionPopup = document.querySelector(".deductionPopup")
const popupBgModulesDeduction = document.querySelector(".popupBgModulesDeduction")
const deductionCloseBtn = document.querySelector(".deductionCloseBtn")
const deductionMoreHidden = document.querySelector(".deductionMoreHidden")
const deductionMoreHiddenMonth = document.querySelector(".deductionMoreHiddenMonth")
const deductionTableScroll = document.querySelector(".deductionTableScroll tbody")
const deductionListAllCheck = document.querySelector(".deductionListAllCheck")

for (i = 0; i < deduction.length; i++) {
    deduction[i].addEventListener("click", openAddSalaryPopup)
};

function openAddSalaryPopup() {
    deductionPopup.style.display = "block"
    deductionMoreHidden.value = this.parentNode.children[0].children[0].value
    deductionMoreHiddenMonth.value = searchMonth.value

    let targetItem = 0
    for (i = 0; i < addSalarly.length; i++) {
        if (addSalarly[i].parentNode === this.parentNode) {
            targetItem = i
        }
    };

    for (i = 0; i < deductionList[targetItem].length; i++) {
        const addTr = document.createElement("tr")
        addTr.setAttribute("class", "table-list_body-tr deductionList")
        deductionTableScroll.appendChild(addTr)

        const addTd1 = document.createElement("td")
        addTd1.setAttribute("class", "table-list_body-tr_td")
        addTr.appendChild(addTd1)

        const addCheckbox = document.createElement("input")
        addCheckbox.setAttribute("type", "checkbox")
        addCheckbox.setAttribute("class", "deductionChecker")
        addCheckbox.setAttribute("value", deductionList[targetItem][i].id)
        addCheckbox.setAttribute("name", "id")
        addTd1.appendChild(addCheckbox)

        const addTd2 = document.createElement("td")
        addTd2.setAttribute("class", "table-list_body-tr_td priceTd")
        addTd2.innerText = deductionList[targetItem][i].price
        addTr.appendChild(addTd2)

        const addTd3 = document.createElement("td")
        addTd3.setAttribute("class", "table-list_body-tr_td")
        addTd3.innerText = deductionList[targetItem][i].remark
        addTr.appendChild(addTd3)
    };

    const price = document.querySelectorAll(".priceTd")
    const deductionTrList = document.querySelectorAll(".deductionList")
    const deductionChecker = document.querySelectorAll(".deductionChecker")
    deductionTotal(price)
    deductionChecking(deductionTrList, deductionChecker)

    deductionListAllCheck.addEventListener("change", checkingAll)

    function checkingAll(){
        if(this.checked){
            for (i = 0; i < deductionChecker.length; i++){
                deductionChecker[i].checked = true
            };
        }else{
            for (i = 0; i < deductionChecker.length; i++){
                deductionChecker[i].checked = false
            };
        }
    }
}


popupBgModulesDeduction.addEventListener("click", closeAddSalaryPopup)
deductionCloseBtn.addEventListener("click", closeAddSalaryPopup)
SidemenuUseClose.addEventListener("click", closeAddSalaryPopup)

function closeAddSalaryPopup() {
    deductionPopup.style.display = "none"
    deductionTableScroll.innerText = ""
}


function deductionTotal(price){
    let TotalAmount = 0
    for (i = 0; i < price.length; i++){
        TotalAmount = TotalAmount + parseInt(price[i].innerText)
        price[i].innerText = price[i].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    };
    totalAddSalaryPrice[1].innerText = TotalAmount
    totalAddSalaryPrice[1].innerText = totalAddSalaryPrice[1].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}



function deductionChecking(deductionTrList, deductionChecker){

    for (i = 0; i < deductionTrList.length; i++){
        deductionTrList[i].addEventListener("click", checkingForList)
    };

    function checkingForList(){
        if(this.children[0].children[0].checked){
            this.children[0].children[0].checked = false
        }else{
            this.children[0].children[0].checked = true
        }
        
        let checker = 0
        for (i = 0; i < deductionChecker.length; i++){
            if(deductionChecker[i].checked){
                checker++
            }
        };
        if(deductionChecker.length === checker){
            deductionListAllCheck.checked = true
        }else{
            deductionListAllCheck.checked = false
        }
    }
    



    for (i = 0; i < deductionChecker.length; i++){
        deductionChecker[i].addEventListener("click", checking)
    };
    
    function checking(e){
        e.stopPropagation()
        let checker = 0
        for (i = 0; i < deductionChecker.length; i++){
            if(deductionChecker[i].checked){
                checker++
            }
        };
        if(deductionChecker.length === checker){
            deductionListAllCheck.checked = true
        }else{
            deductionListAllCheck.checked = false
        }
    }

}