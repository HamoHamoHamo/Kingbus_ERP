const btnModulesCreate = document.querySelector(".btnModulesCreate")
const creteForm = document.querySelector(".creteForm")
let essential = document.querySelectorAll(".essential")
const btnModulesEdit = document.querySelector(".btnModulesEdit")
const editForm = document.querySelector(".editForm")
let essentialEdit = document.querySelectorAll(".essentialEdit")
const removeComma = document.querySelectorAll(".numberOnly")

const paymentSelect = document.querySelector("#paymentSelect")
const editPaymentSelect = document.querySelector("#editPaymentSelect")

const bankName = document.querySelector('#bankName')
const bankNameStar = document.querySelector('#bankNameStar')
const eBankName = document.querySelector('#editBankName')
const editBankNameStar = document.querySelector('#editBankNameStar')


paymentSelect.addEventListener('change', changePayment)

function changePayment(e) {
    if (e.target.value == '현금') {
        bankName.classList.remove('essential');
        bankNameStar.innerText = '';
        essential = document.querySelectorAll(".essential")
    } else {
        bankName.className = 'popupArticleinput length100 essential';
        bankNameStar.innerText = '*';
        essential = document.querySelectorAll(".essential")
    }
}

editPaymentSelect.addEventListener('change', editChangePayment)

function editChangePayment(e) {
    if (e.target.value == '현금') {
        eBankName.classList.remove('essentialEdit');
        editBankNameStar.innerText = '';
        essentialEdit = document.querySelectorAll(".essentialEdit")
    } else {
        eBankName.className = 'popupArticleinput length100 essentialEdit';
        editBankNameStar.innerText = '*';
        essentialEdit = document.querySelectorAll(".essentialEdit")
    }
}

btnModulesCreate.addEventListener("click", createCheck)

function createCheck() {
    for (i = 0; i < essential.length; i++) {
        if (essential[i].value == "") {
            return alert("입력하지 않은 필수 입력사항이 있습니다.")
        }
    };
    removeComma[0].value = removeComma[0].value.replace(/\,/g, "")
    removeComma[1].value = removeComma[1].value.replace(/\,/g, "")
    creteForm.submit()
}

btnModulesEdit.addEventListener("click", editCheck)

function editCheck() {
    for (i = 0; i < essentialEdit.length; i++) {
        if (essentialEdit[i].value == "") {
            return alert("입력하지 않은 필수 입력사항이 있습니다.")
        }
    };
    removeComma[2].value = removeComma[2].value.replace(/\,/g, "")
    removeComma[3].value = removeComma[3].value.replace(/\,/g, "")
    editForm.submit()
}