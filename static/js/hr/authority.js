const salarySaveBtn = document.querySelector(".salarySaveBtn")
const salaryTotalContainer = document.querySelector(".salaryTotalContainer")
const tableBody = document.querySelector(".scrolling_table-list_body")
const amountInput = document.querySelectorAll(".amountInput")

function authority() {
    if (AUTHORITY >= 3) {
        salarySaveBtn.style.display = "none"
        salaryTotalContainer.style.display = "none"
        tableBody.style.height = "72rem"
        for (i = 0; i < amountInput.length; i++) {
            console.log(amountInput[i]);
            amountInput[i].style.border = "none"
            amountInput[i].setAttribute("disabled", "true")
        }
    }
}
authority()