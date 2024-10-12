const meal = document.querySelectorAll(".mealTd")
const mealPopup = document.querySelector(".mealPopup")
const popupBgModulesMeal = document.querySelector(".popupBgModulesMeal")
const mealCloseBtn = document.querySelector(".mealCloseBtn")
const mealMoreHidden = document.querySelector(".mealMoreHidden")
const mealTableScroll = document.querySelector(".mealTableScroll tbody")
const mealListAllCheck = document.querySelector(".mealListAllCheck")

for (i = 0; i < meal.length; i++) {
    meal[i].addEventListener("click", openAddSalaryPopup)
};

function openAddSalaryPopup() {
    mealPopup.style.display = "block"

    let targetItem = 0
    for (i = 0; i < meal.length; i++) {
        if (meal[i].parentNode === this.parentNode) {
            targetItem = i
        }
    };

    for (i = 0; i < mealList[targetItem].length; i++) {
        if (mealList[targetItem][i] == 0) continue;
        const addTr = document.createElement("tr")
        addTr.setAttribute("class", "table-list_body-tr mealList")
        mealTableScroll.appendChild(addTr)

        const addTd2 = document.createElement("td")
        addTd2.setAttribute("class", "table-list_body-tr_td")
        addTd2.innerText = `${i + 1}일`
        addTr.appendChild(addTd2)

        const addTd3 = document.createElement("td")
        addTd3.setAttribute("class", "table-list_body-tr_td priceTd")
        addTd3.innerText = (mealList[targetItem][i])
        addTr.appendChild(addTd3)
    };

    const price = document.querySelectorAll(".priceTd")
    const mealTrList = document.querySelectorAll(".mealList")
    const mealChecker = document.querySelectorAll(".mealChecker")
    mealTotal(price)
    mealChecking(mealTrList, mealChecker)


    mealListAllCheck.addEventListener("change", checkingAll)

    function checkingAll(){
        if(this.checked){
            for (i = 0; i < mealChecker.length; i++){
                mealChecker[i].checked = true
            };
        }else{
            for (i = 0; i < mealChecker.length; i++){
                mealChecker[i].checked = false
            };
        }
    }
}


popupBgModulesMeal.addEventListener("click", closeAddSalaryPopup)
mealCloseBtn.addEventListener("click", closeAddSalaryPopup)
SidemenuUseClose.addEventListener("click", closeAddSalaryPopup)

function closeAddSalaryPopup() {
    mealPopup.style.display = "none"
    mealTableScroll.innerText = ""
}


function mealTotal(price){
    let TotalAmount = 0
    for (i = 0; i < price.length; i++){
        TotalAmount = TotalAmount + parseInt(price[i].innerText)
        price[i].innerText = price[i].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    };
    totalAddSalaryPrice[3].innerText = TotalAmount
    totalAddSalaryPrice[3].innerText = totalAddSalaryPrice[3].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}



function mealChecking(mealTrList, mealChecker){

    for (i = 0; i < mealTrList.length; i++){
        mealTrList[i].addEventListener("click", checkingForList)
    };

    function checkingForList(){
        if(this.children[0].children[0].checked){
            this.children[0].children[0].checked = false
        }else{
            this.children[0].children[0].checked = true
        }
        
        let checker = 0
        for (i = 0; i < mealChecker.length; i++){
            if(mealChecker[i].checked){
                checker++
            }
        };
        if(mealChecker.length === checker){
            mealListAllCheck.checked = true
        }else{
            mealListAllCheck.checked = false
        }
    }
    



    for (i = 0; i < mealChecker.length; i++){
        mealChecker[i].addEventListener("click", checking)
    };
    
    function checking(e){
        e.stopPropagation()
        let checker = 0
        for (i = 0; i < mealChecker.length; i++){
            if(mealChecker[i].checked){
                checker++
            }
        };
        if(mealChecker.length === checker){
            mealListAllCheck.checked = true
        }else{
            mealListAllCheck.checked = false
        }
    }

}