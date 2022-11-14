const editPopupCloseBtn = document.querySelector(".editPopupCloseBtn")
const editDate = document.querySelector(".editDate")
const editDepositType = document.querySelector(".editDepositType")
const editBankName = document.querySelector(".editBankName")
const editVat = document.querySelector(".editVat")
const editDepositPrice = document.querySelector(".editDepositPrice")
const editDepositorName = document.querySelector(".editDepositorName")
const editHidden = document.querySelector(".editHidden")

for (i = 0; i < depositCell.length; i++) {
    depositCell[i].addEventListener("click", editPopup)
};

function editPopup() {
    popupAreaModules[2].style.display = "block"
    let editTarget = ""
    for (i = 0; i < depositCell.length; i++) {
        if (depositCell[i] === this) {
            editTarget = i
        }
    };
    for (i = 0; i < editDepositType.children.length; i++) {
        if (editDepositType.children[i].value === dataList[editTarget].payment_method) {
            editDepositType.children[i].selected = true
        }
    };
    editDate.value = dataList[editTarget].date.split(" ")[0]
    editBankName.value = dataList[editTarget].bank
    editVat.value = dataList[editTarget].commission
    editDepositPrice.value = dataList[editTarget].acc_income
    editDepositorName.value = dataList[editTarget].depositor
    editHidden.value = this.children[0].children[0].value
}

popupBgModules[2].addEventListener("click", closePopupEdit)
SidemenuUseClose.addEventListener("click", closePopupEdit)
editPopupCloseBtn.addEventListener("click", closePopupEdit)

function closePopupEdit() {
    popupAreaModules[2].style.display = "none"
}