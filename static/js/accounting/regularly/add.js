const additionalPopup = document.querySelector(".additionalPopup")
const popupBgModulesAdd = document.querySelector(".popupBgModulesAdd")
const addCloseBtn = document.querySelector(".addCloseBtn")
const addMoreIdHidden = document.querySelector(".addMoreIdHidden")
const addMoreDateHidden = document.querySelector(".addMoreDateHidden")
const searchDate = document.querySelector(".searchTool input[type=month]")
const addListTable = document.querySelector(".addTable tbody")
const addTotalPrice = document.querySelector(".addTotalPrice")
const addTotalVat = document.querySelector(".addTotalVat")
const addTotalTotal = document.querySelector(".addTotalTotal")
const addDeleteBtn = document.querySelector(".addDeleteBtn")
const addListAllCheck = document.querySelector(".addListAllCheck")
const addDeleteForm = document.querySelector(".addDeleteForm")
const amountInput = document.querySelectorAll(".amountInput")
const addForm = document.querySelector(".addForm")
const addBtn = document.querySelector(".addBtn")


for (i = 0; i < collectDateBox.length; i++) {
    collectDateBox[i].children[6].addEventListener("click", openAddPopup)
};

function openAddPopup() {
    additionalPopup.style.display = "block"
    addMoreIdHidden.value = this.parentNode.children[0].children[0].value
    addMoreDateHidden.value = searchDate.value


    let addRoute = 0
    for (i = 0; i < collectDateBox.length; i++) {
        if (this.parentNode === collectDateBox[i]) {
            addRoute = i
        }
    };

    for (i = 0; i < additionalList[addRoute].length; i++) {
        const addListTr = document.createElement("tr")
        addListTr.setAttribute("class", "table-list_body-tr")
        addListTr.setAttribute("onclick", "addListChekingTr(this, event)")
        addListTable.appendChild(addListTr)

        const addListTd1 = document.createElement("td")
        addListTd1.setAttribute("class", "table-list_body-tr_td")
        addListTr.appendChild(addListTd1)

        const addListCheckbox = document.createElement("input")
        addListCheckbox.setAttribute("type", "checkbox")
        addListCheckbox.setAttribute("onclick", "addListCheking(this, event)")
        addListCheckbox.setAttribute("class", "addListCheckbox")
        addListCheckbox.setAttribute("name", "id")
        addListCheckbox.setAttribute("value", `${additionalList[addRoute][i].id}`)
        addListTd1.appendChild(addListCheckbox)

        const addListTd2 = document.createElement("td")
        addListTd2.setAttribute("class", "table-list_body-tr_td")
        addListTd2.innerText = i + 1
        addListTr.appendChild(addListTd2)

        const addListTd3 = document.createElement("td")
        addListTd3.setAttribute("class", "table-list_body-tr_td")
        addListTd3.innerText = additionalList[addRoute][i].category
        addListTr.appendChild(addListTd3)

        const addListTd4 = document.createElement("td")
        addListTd4.setAttribute("class", "table-list_body-tr_td")
        addListTd4.innerText = additionalList[addRoute][i].value
        addListTr.appendChild(addListTd4)

        const addListTd5 = document.createElement("td")
        addListTd5.setAttribute("class", "table-list_body-tr_td")
        addListTd5.innerText = additionalList[addRoute][i].VAT
        addListTr.appendChild(addListTd5)

        const addListTd6 = document.createElement("td")
        addListTd6.setAttribute("class", "table-list_body-tr_td")
        addListTd6.innerText = additionalList[addRoute][i].total_price
        addListTr.appendChild(addListTd6)

        const addListTd7 = document.createElement("td")
        addListTd7.setAttribute("class", "table-list_body-tr_td")
        addListTd7.innerText = additionalList[addRoute][i].note
        addListTr.appendChild(addListTd7)
    };

    const addListTr = document.querySelectorAll(".scrolling_table-list_body .table-list_body-tr")

    for (i = 0; i < addListTr.length; i++) {
        addListTr[i].children[3].innerText = addListTr[i].children[3].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        addListTr[i].children[4].innerText = addListTr[i].children[4].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        addListTr[i].children[5].innerText = addListTr[i].children[5].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    };

    let price = 0
    let vat = 0

    for (i = 0; i < addListTr.length; i++) {
        price = price + parseInt(addListTr[i].children[3].innerText.replace(/\,/g, ""))
        vat = vat + parseInt(addListTr[i].children[4].innerText.replace(/\,/g, ""))
    };

    addTotalPrice.innerText = price
    addTotalVat.innerText = vat
    addTotalTotal.innerText = price + vat

    addTotalPrice.innerText = addTotalPrice.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    addTotalVat.innerText = addTotalVat.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    addTotalTotal.innerText = addTotalTotal.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}

popupBgModulesAdd.addEventListener("click", clodeAddPopup)
addCloseBtn.addEventListener("click", clodeAddPopup)
SidemenuUseClose.addEventListener("click", clodeAddPopup)

function clodeAddPopup() {
    additionalPopup.style.display = "none"
    addListTable.innerText = ""
}


addDeleteBtn.addEventListener("click", deleteAdd)

function deleteAdd() {
    const addListCheckbox = document.querySelectorAll(".addListCheckbox")
    let checkChecker = false
    for (i = 0; i < addListCheckbox.length; i++) {
        if (addListCheckbox[i].checked) {
            checkChecker = true
        }
    };
    if (checkChecker) {
        addDeleteForm.submit();
    } else {
        alert("삭제할 항목을 선택해 주세요")
    }
}


function addListChekingTr(addChecker, event) {
    event.stopPropagation()
    const addListCheckbox = document.querySelectorAll(`.${addChecker.children[0].children[0].classList[0]}`)

    if (addChecker.children[0].children[0].checked) {
        addChecker.children[0].children[0].checked = false
    } else {
        addChecker.children[0].children[0].checked = true
    }

    let addCheckCount = 0
    for (i = 0; i < addListCheckbox.length; i++) {
        if (addListCheckbox[i].checked) {
            addCheckCount++
        }
    }
    if (addCheckCount === addListCheckbox.length) {
        addListAllCheck.checked = true
    } else {
        addListAllCheck.checked = false
    }
}

function addListCheking(addChecker, event) {
    event.stopPropagation()
    const addListCheckbox = document.querySelectorAll(`.${addChecker.classList[0]}`)
    let addCheckCount = 0
    for (i = 0; i < addListCheckbox.length; i++) {
        if (addListCheckbox[i].checked) {
            addCheckCount++
        }
    }
    if (addCheckCount === addListCheckbox.length) {
        addListAllCheck.checked = true
    } else {
        addListAllCheck.checked = false
    }
}

addListAllCheck.addEventListener("change", addListAllChcecker)

function addListAllChcecker() {
    const addListCheckbox = document.querySelectorAll(".addListCheckbox")
    if (this.checked) {
        for (i = 0; i < addListCheckbox.length; i++) {
            addListCheckbox[i].checked = true
        };
    } else {
        for (i = 0; i < addListCheckbox.length; i++) {
            addListCheckbox[i].checked = false
        };
    }
}




for (i = 0; i < amountInput.length; i++) {
    amountInput[i].addEventListener("input", onlyNum)
    amountInput[i].addEventListener("click", removeComma)
    amountInput[i].addEventListener("focusout", makeResult)
};

function removeComma() {
    this.value = this.value.replace(/\,/g, "")
}

function onlyNum() {
    let check = /^[0-9]+$/
    let regex = /[^0-9]/g;
    if (!check.test(this.value)) {
        this.value = this.value.replace(regex, "")
    }
}


function makeResult(){
    let result = this.value;
    targetInput = this
    remove0(result, targetInput)
}


function remove0(result, targetInput){
    if(result.length > 1){
        if(result[0] == 0){
            result = result.substr(1,)
            remove0(result, targetInput)
        }else{
            changeAddComma(result, targetInput)
        }
    }
}


function changeAddComma(result, targetInput){
    targetInput.value = result
    targetInput.value = targetInput.value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}


addBtn.addEventListener("click", addSubmit)

function addSubmit(){
    amountInput[0].value = amountInput[0].value.replace(/\,/g, "")
    amountInput[1].value = amountInput[1].value.replace(/\,/g, "")
    addForm.submit()
}