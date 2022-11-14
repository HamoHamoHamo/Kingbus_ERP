const collectUnprocessed = document.querySelector("#collectUnprocessed")
const collectprocessed = document.querySelector("#collectprocessed")
const collectionProcessed = document.querySelectorAll(".collectionProcessed")
const collectionUnprocessed = document.querySelectorAll(".collectionUnprocessed")


collectUnprocessed.addEventListener("change", visibleUnprocessed)

function visibleUnprocessed() {
    if (collectUnprocessed.checked) {
        for (i = 0; i < collectionUnprocessed.length; i++) {
            collectionUnprocessed[i].classList.remove("tRdisplayNone")
        };
    } else {
        for (i = 0; i < collectionUnprocessed.length; i++) {
            collectionUnprocessed[i].classList.add("tRdisplayNone")
        };
        collectprocessed.checked = true
        visibleProcessed()
    }
    calcTotal(collectUnprocessed.checked, collectprocessed.checked)
}


collectprocessed.addEventListener("change", visibleProcessed)

function visibleProcessed() {
    if (collectprocessed.checked) {
        for (i = 0; i < collectionProcessed.length; i++) {
            collectionProcessed[i].classList.remove("tRdisplayNone")
        };
    } else {
        for (i = 0; i < collectionProcessed.length; i++) {
            collectionProcessed[i].classList.add("tRdisplayNone")
        };
        collectUnprocessed.checked = true
        visibleUnprocessed()
    }
    calcTotal(collectUnprocessed.checked, collectprocessed.checked)
}

calcTotal(collectUnprocessed.checked, collectprocessed.checked)