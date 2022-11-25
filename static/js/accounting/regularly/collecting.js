const loadDepositBtn = document.querySelector(".loadDepositBtn")
const collectingPopupAreaModules = document.querySelector(".collectingPopupAreaModules")
const collectPopupCloseBtn = document.querySelector(".collectPopupCloseBtn")
const popupBgModulesCollect = document.querySelector(".popupBgModulesCollect")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const loadDate = document.querySelectorAll(".collectingPopupContainer .popupSearch input")
const popupBody = document.querySelector(".collectingPopupContainer .popupBody")
const collectingSearch = document.querySelector(".collectingSearch")
const depositorInput = document.querySelector(".depositorInput")
const loadTable = document.querySelector(".collectingPopupScrollBox table")
const collectPopupRegistrationBtn = document.querySelector(".collectPopupRegistrationBtn")
const collectingPopupContainer = document.querySelector(".collectingPopupContainer")
const month = document.querySelector(".searchTool input[type=month]")
const collectionMonth = document.querySelector(".collectionMonth")


let toatalAccountsReceivable = 0
let selectGroup = false
let checkCount = 0

// 팝업열기
loadDepositBtn.addEventListener("click", openLoadPopup)

function openLoadPopup(){
    
    collectionMonth.value = month.value
    
    toatalAccountsReceivable = 0
    for (i = 0; i < routeSelect.length; i++) {
        if (routeSelect[i].checked) {
            const hiddenId = document.createElement("input")
            hiddenId.setAttribute("type", "hidden")
            hiddenId.setAttribute("class", "loadDepositHidden")
            hiddenId.setAttribute("name", "group_id")
            hiddenId.setAttribute("value", `${routeSelect[i].value}`)
            popupBody.appendChild(hiddenId)
            selectGroup = true
            toatalAccountsReceivable = toatalAccountsReceivable + parseInt(routeSelect[i].parentNode.parentNode.children[10].innerText.replace(/\,/g, ""))
            checkCount++
        }
    };
    if(selectGroup){
        collectingPopupAreaModules.style.display = "block"

        let today = new Date();

        let year = today.getFullYear();
        let month = today.getMonth() + 1;
        let date = today.getDate();

        loadDate[0].value = `${year}-${month}-01`
        loadDate[1].value = `${year}-${month}-${date}`
    }else{
        alert("그룹을 선택해 주세요")
    }
}

// 팝업닫기
collectPopupCloseBtn.addEventListener("click", closeLoadPopup)
popupBgModulesCollect.addEventListener("click", closeLoadPopup)
SidemenuUseClose.addEventListener("click", closeLoadPopup)

function closeLoadPopup(){
    collectingPopupAreaModules.style.display = "none"
    const hiddenId = document.querySelectorAll(".loadDepositHidden")
    for (i = 0; i < hiddenId.length; i++) {
        hiddenId[i].remove()
    };
}

// 검색
collectingSearch.addEventListener("click", searchDeposit)

function searchDeposit() {

    let communicationData = {
        date1: loadDate[0].value,
        date2: loadDate[1].value,
        depositor: depositorInput.value
    }
    $.ajax({
        url: "/accounting/collect/load",
        method: "POST",
        data: JSON.stringify(communicationData),
        datatype: 'json',
        success: function (result) {
            if (result.status) {
                console.log(result.deposit);

                loadTable.innerText = ""
                for (i = 0; i < result.deposit.length; i++) {
                    const loadTr = document.createElement("tr")
                    loadTr.setAttribute("class", "depositItem")
                    loadTable.appendChild(loadTr)

                    const loadTd1 = document.createElement("td")
                    loadTr.appendChild(loadTd1)

                    const radioBox1 = document.createElement("input")
                    radioBox1.setAttribute("type", "radio")
                    radioBox1.setAttribute("value", `${result.deposit[i].id}`)
                    radioBox1.setAttribute("name", "income_id")
                    loadTd1.appendChild(radioBox1)

                    const radioBox2 = document.createElement("td")
                    radioBox2.innerText = result.deposit[i].serial
                    loadTr.appendChild(radioBox2)

                    const radioBox3 = document.createElement("td")
                    radioBox3.innerText = result.deposit[i].date
                    loadTr.appendChild(radioBox3)

                    const radioBox4 = document.createElement("td")
                    radioBox4.innerText = result.deposit[i].payment_method
                    loadTr.appendChild(radioBox4)

                    const radioBox5 = document.createElement("td")
                    radioBox5.innerText = result.deposit[i].total_income.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
                    loadTr.appendChild(radioBox5)

                    const radioBox6 = document.createElement("td")
                    radioBox6.innerText = result.deposit[i].depositor
                    loadTr.appendChild(radioBox6)

                    const radioBox7 = document.createElement("td")
                    radioBox7.innerText = parseInt(result.deposit[i].total_income) - parseInt(result.deposit[i].used_price)
                    radioBox7.innerText = radioBox7.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
                    loadTr.appendChild(radioBox7)

                    const depositItem = document.querySelectorAll(".depositItem")
                    clickFunction(depositItem)
                };
            } else {
                alert("입금내역을 불러오지 못했습니다.")
            }
        },
        error: function (request, error) {
            console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
        },
    });

}

function clickFunction(loadList) {

    for (j = 0; j < loadList.length; j++) {
        loadList[j].addEventListener("click", selectLoadItem)
    };

    function selectLoadItem() {
        this.children[0].children[0].checked = true
    }
}


collectPopupRegistrationBtn.addEventListener("click", priceCheck)

function priceCheck() {
    let balance = 0
    const loadRadio = document.querySelectorAll(".collectingPopupScrollBox input[name=income_id]")
    for (i = 0; i < loadRadio.length; i++) {
        if (loadRadio[i].checked) {
            balance = loadRadio[i].parentNode.parentNode.children[6].innerText.replace(/\,/g, "")
        }
    };
    if (balance < toatalAccountsReceivable && checkCount !== 1) {
        alert("잔액이 부족합니다.")
    } else {
        collectingPopupContainer.submit();
    }
}


document.addEventListener('keydown', function (event) {
    if (event.keyCode === 13 && collectingPopupAreaModules.style.display === "block") {
        event.preventDefault();
        searchDeposit()
    };
}, true);