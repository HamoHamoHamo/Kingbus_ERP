const searchAccount = document.querySelector(".searchAccount")
const accountCloseBtn = document.querySelector(".accountCloseBtn")
const loadAccountBtn = document.querySelector(".loadAccountBtn")
const accountTable = document.querySelector(".accountTable tbody")
const loadClient = document.querySelector(".loadClient")
const loadPhone = document.querySelector(".loadPhone")
const accountSelect = document.querySelector(".accountSelect")
const accountInput = document.querySelector(".accountInput")
const accountSearchBtn = document.querySelector(".accountSearchBtn")

searchAccount.addEventListener("click", openAccounting)

function openAccounting() {
    popupAreaModules[2].style.display = "block"

    for (i = 0; i < client.length; i++) {
        const accountTr = document.createElement("tr")
        accountTr.setAttribute("class", "table-list_body-tr accountTr")
        accountTr.setAttribute("style", "cursor: pointer;")
        accountTable.appendChild(accountTr)

        const accounTd1 = document.createElement("td")
        accounTd1.setAttribute("class", "table-list_body-tr_td")
        accountTr.appendChild(accounTd1)

        const accounCheckbox = document.createElement("input")
        accounCheckbox.setAttribute("class", "accountCheckbox")
        accounCheckbox.setAttribute("type", "radio")
        accounCheckbox.setAttribute("name", "account")
        accounCheckbox.setAttribute("value", `${i}`)
        accounTd1.appendChild(accounCheckbox)

        const accounTd2 = document.createElement("td")
        accounTd2.setAttribute("class", "table-list_body-tr_td")
        accounTd2.innerText = client[i].name
        accountTr.appendChild(accounTd2)

        const accounTd3 = document.createElement("td")
        accounTd3.setAttribute("class", "table-list_body-tr_td")
        accounTd3.innerText = client[i].phone
        accountTr.appendChild(accounTd3)
    };

    const accountTr = document.querySelectorAll(".accountTr");
    loadAccountBtn.addEventListener("click", loadAccount)

    function loadAccount() {
        for (i = 0; i < accountTr.length; i++){
            if(accountTr[i].children[0].children[0].checked){
                loadClient.value = accountTr[i].children[1].innerText
                loadPhone.value = accountTr[i].children[2].innerText
                return closeAccounting()
            }
        };
        alert("불러올 거래처 정보를 선택해 주세요.")
    }

    for (i = 0; i < accountTr.length; i++){
        accountTr[i].addEventListener("click", checkingRadio)
    };

    function checkingRadio(){
        this.children[0].children[0].checked = true
    }

    accountSearchBtn.addEventListener("click", filterAccount)

    function filterAccount(){
        if(accountSelect.options[accountSelect.selectedIndex].value === "거래처명"){
            accountFilterling(accountTr, accountInput.value)
        }else{
            phoneNumFilterling(accountTr, accountInput.value)
        }        
    }
}

accountCloseBtn.addEventListener("click", closeAccounting)
popupBgModules[2].addEventListener("click", closeAccounting)
SidemenuUseClose.addEventListener("click", closeAccounting)

function closeAccounting() {
    popupAreaModules[2].style.display = "none"
    accountTable.innerText = ""
}

function accountFilterling(accountTr, text){
    for (i = 0; i < accountTr.length; i++){
        accountTr[i].style.display = "table-row"
    };
    for (i = 0; i < accountTr.length; i++){
        if(!accountTr[i].children[1].innerText.includes(text)){
            accountTr[i].style.display = "none"
        }
    };    
}

function phoneNumFilterling(accountTr, text){
    for (i = 0; i < accountTr.length; i++){
        accountTr[i].style.display = "table-row"
    };
    for (i = 0; i < accountTr.length; i++){
        if(!accountTr[i].children[2].innerText.includes(text)){
            accountTr[i].style.display = "none"
        }
    };    
}