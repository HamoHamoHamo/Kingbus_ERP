const historyPopupAreaModules = document.querySelector(".historyPopupAreaModules")
const popupBgModulesHistory = document.querySelector(".popupBgModulesHistory")
const historyPopupCloseBtn = document.querySelector(".historyPopupCloseBtn")
const chitList = document.querySelector(".historyingPopupScrollBox table")

for (i = 0; i < collectDateBox.length; i++) {
    collectDateBox[i].children[8].addEventListener("click", openHistoryPopup)
};

function openHistoryPopup() {
    if (this.innerText !== "") {
        historyPopupAreaModules.style.display = "block"
        chitList.innerText = ""
    }
    
    let targetChit = ""
    for (i = 0; i < collectDateBox.length; i++) {
        if (this.parentNode === collectDateBox[i]) {
            targetChit = i
        }
    };

    for (i = 0; i < incomeList[targetChit].length; i++) {
        const chitTr = document.createElement("tr")
        chitList.appendChild(chitTr)

        const chitTrtd1 = document.createElement("td")
        chitTr.appendChild(chitTrtd1)

        const checkbox = document.createElement("input")
        checkbox.setAttribute("type", "checkbox")
        checkbox.setAttribute("value", `${incomeList[targetChit][i].id}`)
        checkbox.setAttribute("name", "id")
        chitTrtd1.appendChild(checkbox)
        const chitTrtd2 = document.createElement("td")
        chitTrtd2.innerText = i + 1
        chitTr.appendChild(chitTrtd2)

        const chitTrtd3 = document.createElement("td")
        chitTrtd3.innerText = incomeList[targetChit][i].serial
        chitTr.appendChild(chitTrtd3)

        const chitTrtd4 = document.createElement("td")
        chitTrtd4.innerText = incomeList[targetChit][i].date
        chitTr.appendChild(chitTrtd4)

        const chitTrtd5 = document.createElement("td")
        chitTrtd5.innerText = incomeList[targetChit][i].depositor
        chitTr.appendChild(chitTrtd5)

        const chitTrtd6 = document.createElement("td")
        chitTrtd6.innerText = incomeList[targetChit][i].payment_method
        chitTr.appendChild(chitTrtd6)

        const chitTrtd7 = document.createElement("td")
        chitTrtd7.innerText = incomeList[targetChit][i].bank
        chitTr.appendChild(chitTrtd7)

        const chitTrtd8 = document.createElement("td")
        chitTrtd8.innerText = incomeList[targetChit][i].commission.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        chitTr.appendChild(chitTrtd8)

        const chitTrtd9 = document.createElement("td")
        chitTrtd9.innerText = incomeList[targetChit][i].acc_income.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        chitTr.appendChild(chitTrtd9)

        const chitTrtd10 = document.createElement("td")
        chitTrtd10.innerText = incomeList[targetChit][i].price.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        chitTr.appendChild(chitTrtd10)

        const chitTrtd11 = document.createElement("td")
        chitTrtd11.innerText = incomeList[targetChit][i].state
        chitTr.appendChild(chitTrtd11)
    };

    const chitListItem = document.querySelectorAll(".historyingPopupScrollBox tr")
    const checkAll = document.querySelector(".historyingPopupHeader input")
    const checkOne = document.querySelectorAll(".historyingPopupScrollBox input")

    for (i = 0; i < chitListItem.length; i++) {
        chitListItem[i].addEventListener("click", checking)
    };

    function checking() {
        let checkCount = 0

        if(this.children[0].children[0].checked){
            this.children[0].children[0].checked = false
        }else{
            this.children[0].children[0].checked = true
        }

        for (i = 0; i < checkOne.length; i++){
            if(checkOne[i].checked){
                checkCount++
            }            
        };
        if(checkCount === checkOne.length){
            checkAll.checked = true
        }else{
            checkAll.checked = false
        }
    }
    
    for (i = 0; i < checkOne.length; i++) {
        checkOne[i].addEventListener("click", checkingCheckbox)
    };

    function checkingCheckbox(e){
        e.stopPropagation()
        let checkCount = 0
        
        for (i = 0; i < checkOne.length; i++){
            if(checkOne[i].checked){
                checkCount++
            }            
        };
        if(checkCount === checkOne.length){
            checkAll.checked = true
        }else{
            checkAll.checked = false
        }
    }
    
    checkAll.addEventListener("change", checkingAll)

    function checkingAll(){
        if(!this.checked){
            for (i = 0; i < checkOne.length; i++){
                checkOne[i].checked = false
            };
        }else{
            for (i = 0; i < checkOne.length; i++){
                checkOne[i].checked = true
            };
        }
    }
}

popupBgModulesHistory.addEventListener("click", clodeHistoryPopup)
historyPopupCloseBtn.addEventListener("click", clodeHistoryPopup)
SidemenuUseClose.addEventListener("click", clodeHistoryPopup)

function clodeHistoryPopup() {
    historyPopupAreaModules.style.display = "none"
}