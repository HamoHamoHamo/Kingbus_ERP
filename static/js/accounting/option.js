const unprocessed = document.querySelector("#unprocessed")
const processed = document.querySelector("#processed")
const depositProcessedCell = document.querySelectorAll(".depositProcessedCell")
const depositUnprocessedCell = document.querySelectorAll(".depositUnprocessedCell")

unprocessed.addEventListener("change", visibleUnprocessed)

function visibleUnprocessed() {
    for (i = 0; i < depositCell.length; i++) {
        depositCell[i].classList.remove("selecting")
    };
    selectTotal.innerText = 0

    if (unprocessed.checked) {
        for (i = 0; i < depositUnprocessedCell.length; i++) {
            depositUnprocessedCell[i].classList.remove("tRdisplayNone")
        };
    } else {
        for (i = 0; i < depositUnprocessedCell.length; i++) {
            depositUnprocessedCell[i].classList.add("tRdisplayNone")
        };
        processed.checked = true
        visibleProcessed()
    }
    calcTotal()
}


processed.addEventListener("change", visibleProcessed)

function visibleProcessed() {
    for (i = 0; i < depositCell.length; i++) {
        depositCell[i].classList.remove("selecting")
    };
    selectTotal.innerText = 0

    if (processed.checked) {
        for (i = 0; i < depositProcessedCell.length; i++) {
            depositProcessedCell[i].classList.remove("tRdisplayNone")
        };
    } else {
        for (i = 0; i < depositProcessedCell.length; i++) {
            depositProcessedCell[i].classList.add("tRdisplayNone")
        };
        unprocessed.checked = true
        visibleUnprocessed()
    }
    calcTotal()
}