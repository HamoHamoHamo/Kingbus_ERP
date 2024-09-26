const addSalarly = document.querySelectorAll(".additionalTd")
const addSalaryPopup = document.querySelector(".addSalaryPopup")
const popupBgModulesAddSalary = document.querySelector(".popupBgModulesAddSalary")
const addSalaryCloseBtn = document.querySelector(".addSalaryCloseBtn")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const addSalaryMoreHidden = document.querySelector(".addSalaryMoreHidden")
const addSalaryMoreHiddenMonth = document.querySelector(".addSalaryMoreHiddenMonth")
const searchMonth = document.querySelector(".search-Form_input-Month")
const addSalaryTable = document.querySelector(".addSalaryTableScroll tbody")
const totalAddSalaryPrice = document.querySelectorAll(".totalAddSalaryPrice")
const addSalaryListAllCheck = document.querySelector(".addSalaryListAllCheck")
const addSalaryDeleteBtn = document.querySelector(".addSalaryDeleteBtn")
const addSalaryDeleteForm = document.querySelector(".addSalaryDeleteForm")

for (i = 0; i < addSalarly.length; i++) {
    addSalarly[i].addEventListener("click", openAddSalaryPopup)
};

function openAddSalaryPopup() {
    addSalaryPopup.style.display = "block"
    addSalaryMoreHidden.value = this.parentNode.children[0].children[0].value
    addSalaryMoreHiddenMonth.value = searchMonth.value

    let targetItem = 0
    for (i = 0; i < addSalarly.length; i++) {
        if (addSalarly[i].parentNode === this.parentNode) {
            targetItem = i
        }
    };

    for (i = 0; i < additionalList[targetItem].length; i++) {
        const addTr = document.createElement("tr")
        addTr.setAttribute("class", "table-list_body-tr addList")
        addSalaryTable.appendChild(addTr)

        const addTd1 = document.createElement("td")
        addTd1.setAttribute("class", "table-list_body-tr_td")
        addTr.appendChild(addTd1)

        const addCheckbox = document.createElement("input")
        addCheckbox.setAttribute("type", "checkbox")
        addCheckbox.setAttribute("class", "addChecker")
        addCheckbox.setAttribute("value", additionalList[targetItem][i].id)
        addCheckbox.setAttribute("name", "id")
        addTd1.appendChild(addCheckbox)

        const addTd2 = document.createElement("td")
        addTd2.setAttribute("class", "table-list_body-tr_td priceTd")
        addTd2.innerText = additionalList[targetItem][i].price
        addTr.appendChild(addTd2)

        const addTd3 = document.createElement("td")
        addTd3.setAttribute("class", "table-list_body-tr_td")
        addTd3.innerText = additionalList[targetItem][i].remark
        addTr.appendChild(addTd3)
    };

    const price = document.querySelectorAll(".priceTd")
    const addList = document.querySelectorAll(".addList")
    const addChecker = document.querySelectorAll(".addChecker")

    addTotal(price)
    addChecking(addList, addChecker)

    addSalaryDeleteBtn.addEventListener("click", addDeleteAdd)


    function addDeleteAdd() {
        for (i = 0; i < addChecker.length; i++) {
            if (addChecker[i].checked) {
                if (confirm('정말로 삭제하시겠습니까?')) {
                    return addSalaryDeleteForm.submit()
                }
                else return;
            }
        };
        return alert("삭제할 항목을 선택해 주세요.")
    }

    addSalaryListAllCheck.addEventListener("change", checkingAll)

    function checkingAll() {
        if (this.checked) {
            for (i = 0; i < addChecker.length; i++) {
                addChecker[i].checked = true
            };
        } else {
            for (i = 0; i < addChecker.length; i++) {
                addChecker[i].checked = false
            };
        }
    }
}


popupBgModulesAddSalary.addEventListener("click", closeAddSalaryPopup)
addSalaryCloseBtn.addEventListener("click", closeAddSalaryPopup)
SidemenuUseClose.addEventListener("click", closeAddSalaryPopup)

function closeAddSalaryPopup() {
    addSalaryPopup.style.display = "none"
    addSalaryTable.innerText = ""
}


function addTotal(price) {
    let TotalAmount = 0
    for (i = 0; i < price.length; i++) {
        TotalAmount = TotalAmount + parseInt(price[i].innerText)
        price[i].innerText = price[i].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    };
    totalAddSalaryPrice[0].innerText = TotalAmount
    totalAddSalaryPrice[0].innerText = totalAddSalaryPrice[0].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}


function addChecking(addList, addChecker) {

    for (i = 0; i < addList.length; i++) {
        addList[i].addEventListener("click", checkingForList)
    };

    function checkingForList() {
        if (this.children[0].children[0].checked) {
            this.children[0].children[0].checked = false
        } else {
            this.children[0].children[0].checked = true
        }

        let checker = 0
        for (i = 0; i < addChecker.length; i++) {
            if (addChecker[i].checked) {
                checker++
            }
        };
        if (addChecker.length === checker) {
            addSalaryListAllCheck.checked = true
        } else {
            addSalaryListAllCheck.checked = false
        }
    }




    for (i = 0; i < addChecker.length; i++) {
        addChecker[i].addEventListener("click", checking)
    };

    function checking(e) {
        e.stopPropagation()
        let checker = 0
        for (i = 0; i < addChecker.length; i++) {
            if (addChecker[i].checked) {
                checker++
            }
        };
        if (addChecker.length === checker) {
            addSalaryListAllCheck.checked = true
        } else {
            addSalaryListAllCheck.checked = false
        }
    }

}