const loadDepositBtn = document.querySelector(".loadDepositBtn")
const routeRadio = document.querySelectorAll(".routeSelect")
const collectingPopupAreaModules = document.querySelector(".collectingPopupAreaModules")
const popupBgModulesCollect = document.querySelector(".popupBgModulesCollect")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const collectPopupCloseBtn = document.querySelector(".collectPopupCloseBtn")
const targetDeposit = document.querySelectorAll(".collectingPopupScrollBox tr")
const loadDate = document.querySelectorAll(".collectingPopupContainer .popupSearch input")
const loadDepositHidden = document.querySelector(".loadDepositHidden")
const collectingSearch = document.querySelector(".collectingSearch")
const loadTable = document.querySelector(".collectingPopupScrollBox table")

loadDepositBtn.addEventListener("click", loadDeposit)

function loadDeposit() {
    let selectRoute = false
    let routeId = ""
    for (i = 0; i < routeRadio.length; i++) {
        if (routeRadio[i].checked) {
            selectRoute = true
            routeId = routeRadio[i].parentNode.parentNode.classList[2]
            break;
        }
    };
    if (selectRoute) {
        collectingPopupAreaModules.style.display = "block"
        loadDepositHidden.value = routeId


        let today = new Date();

        let year = today.getFullYear();
        let month = today.getMonth() + 1;
        let date = today.getDate();

        loadDate[0].value = `${year}-${month}-${date}`
        loadDate[1].value = `${year}-${month}-${date}`

        searchDeposit()

    } else {
        alert("노선을 선택해 주세요")
    }
}

for (i = 0; i < collectDateBox.length; i++) {
    collectDateBox[i].addEventListener("click", routeSelecting)
};

function routeSelecting() {
    this.children[0].children[0].checked = true
}


//팝업닫기
popupBgModulesCollect.addEventListener("click", closePopup)
collectPopupCloseBtn.addEventListener("click", closePopup)
SidemenuUseClose.addEventListener("click", closePopup)

function closePopup() {
    collectingPopupAreaModules.style.display = "none"
}



// 입금내역 선택
for (i = 0; i < targetDeposit.length; i++) {
    targetDeposit[i].addEventListener("click", selectDeposit)
};

function selectDeposit() {
    for (i = 0; i < targetDeposit.length; i++) {
        this.classList.remove("selectDepoditTr")
    };
    this.classList.add("selectDepoditTr")
}



collectingSearch.addEventListener("click", searchDeposit)

function searchDeposit() {

    let communicationData = {
        date1: loadDate[0].value,
        date2: loadDate[1].value,
    }
    $.ajax({
        url: "/accounting/collect/load",
        method: "POST",
        data: JSON.stringify(communicationData),
        datatype: 'json',
        success: function (result) {
            if (result.status) {
                result.deposit
                console.log(result.deposit);

                loadTable.innerText = ""
                for (i = 0; i < result.deposit.length; i++){
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

function clickFunction(loadList){
    
    for (i = 0; i < loadList.length; i++){
        loadList[i].addEventListener("click", selectLoadItem)
    };
    
    function selectLoadItem(){
        this.children[0].children[0].checked = true
    }
}