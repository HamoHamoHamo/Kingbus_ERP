const allChecker = document.querySelector(".allChecker")
const checker = document.querySelectorAll(".checker")
const unprocessed = document.querySelector("#unprocessed")
const processed = document.querySelector("#processed")
const deleteCheck = document.querySelector("#delete")
const depositDeleteBtn = document.querySelector(".depositDeleteBtn")
const depositForm = document.querySelector(".depositForm")

function state() {
    for (i = 0; i < depositCell.length; i++) {
        let targetState = depositCell[i].children[depositCell[i].children.length - 1].innerText
        if (targetState == "미처리") {
            depositCell[i].children[depositCell[i].children.length - 1].classList.add("stateUnprocessed")
        } else if (targetState == "완료") {
            depositCell[i].children[depositCell[i].children.length - 1].classList.add("stateCompletopn")
        }
    };
}
state()

unprocessed.addEventListener("change", optionUnprocessed)
processed.addEventListener("change", optionProcessed)
deleteCheck.addEventListener("change", optionDelete)

function optionUnprocessed() {
    if (this.checked) {
        depositForm.action = "/accounting/deposit/hide"
        deleteCheck.checked = false
    }
    stateOPtion()
    allChecker.checked = false
    for (i = 0; i < checker.length; i++) {
        checker[i].checked = false
    };
    selectArr = []
    totalSelecting(selectArr)
}

function optionProcessed() {
    if (this.checked) {
        depositForm.action = "/accounting/deposit/hide"
        deleteCheck.checked = false
    }
    stateOPtion()
    allChecker.checked = false
    for (i = 0; i < checker.length; i++) {
        checker[i].checked = false
    };
    selectArr = []
    totalSelecting(selectArr)
}

function optionDelete() {
    if (this.checked) {
        depositForm.action = "/accounting/deposit/delete"
        unprocessed.checked = false
        processed.checked = false
    }
    stateOPtion()
    allChecker.checked = false
    for (i = 0; i < checker.length; i++) {
        checker[i].checked = false
    };
    selectArr = []
    totalSelecting(selectArr)
}



function stateOPtion() {
    for (i = 0; i < depositCell.length; i++) {

        if (!unprocessed.checked && depositCell[i].children[9].classList.contains("stateUnprocessed")) {
            depositCell[i].style.display = "none"
        } else if (unprocessed.checked && depositCell[i].children[9].classList.contains("stateUnprocessed")) {
            depositCell[i].style.display = "table-row"
        }

        if (!processed.checked && depositCell[i].children[9].classList.contains("stateCompletopn")) {
            depositCell[i].style.display = "none"
        } else if (processed.checked && depositCell[i].children[9].classList.contains("stateCompletopn")) {
            depositCell[i].style.display = "table-row"
        }

        if (!deleteCheck.checked && !depositCell[i].classList.contains("stateDelete")) {
            depositCell[i].classList.add("stateDelete")
        } else if (deleteCheck.checked && depositCell[i].classList.contains("stateDelete")) {
            depositCell[i].classList.remove("stateDelete")
        }
    };

    separating(unprocessed.checked, processed.checked, deleteCheck.checked)

    calcTotal()

}

stateOPtion()