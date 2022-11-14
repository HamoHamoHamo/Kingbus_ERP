const history = document.querySelectorAll(".collectDateBox td:nth-child(12)")
const historyPopupAreaModules = document.querySelector(".historyPopupAreaModules")
const popupBgModulesHistory = document.querySelector(".popupBgModulesHistory")
const historyPopupCloseBtn = document.querySelector(".historyPopupCloseBtn")
const chitList = document.querySelector(".historyingPopupScrollBox table")

for (i = 0; i < history.length; i++) {
    history[i].addEventListener("click", openHistory)
};

function openHistory() {
    historyPopupAreaModules.style.display = "block"

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
        chitTrtd8.innerText = incomeList[targetChit][i].commission
        chitTr.appendChild(chitTrtd8)

        const chitTrtd9 = document.createElement("td")
        chitTrtd9.innerText = incomeList[targetChit][i].acc_income
        chitTr.appendChild(chitTrtd9)

        const chitTrtd10 = document.createElement("td")
        chitTrtd10.innerText = incomeList[targetChit][i].price
        chitTr.appendChild(chitTrtd10)

        const chitTrtd11 = document.createElement("td")
        chitTrtd11.innerText = incomeList[targetChit][i].state
        chitTr.appendChild(chitTrtd11)
    };

    const chitListItem = document.querySelectorAll(".historyingPopupScrollBox tr")

    for (i = 0; i < chitListItem.length; i++) {
        chitListItem[i].addEventListener("click", checkingCheckbox)
    };

    function checkingCheckbox() {
        if(this.children[0].children[0].checked){
            this.children[0].children[0].checked = false
        }else{
            this.children[0].children[0].checked = true
        }
    }
}



//팝업닫기
popupBgModulesHistory.addEventListener("click", closePopupHistory)
historyPopupCloseBtn.addEventListener("click", closePopupHistory)
SidemenuUseClose.addEventListener("click", closePopupHistory)


function closePopupHistory() {
    historyPopupAreaModules.style.display = "none"
    chitList.innerText = ""
}
