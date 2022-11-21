const collectUnprocessed = document.querySelector("#collectUnprocessed")
const collectprocessed = document.querySelector("#collectprocessed")

collectUnprocessed.addEventListener("change", optionUnprocessed)

function optionUnprocessed() {
    if (this.checked && collectprocessed.checked) {
        for (i = 0; i < collectDateBox.length; i++) {
            if (collectDateBox[i].children[9].classList.contains("unprocessed")) {
                collectDateBox[i].classList.remove("tRdisplayNone")
            }
        };
    } else if (!this.checked && collectprocessed.checked) {
        for (i = 0; i < collectDateBox.length; i++) {
            if (collectDateBox[i].children[9].classList.contains("unprocessed")) {
                collectDateBox[i].classList.add("tRdisplayNone")
            }
        };
    } else if (!this.checked && !collectprocessed.checked) {
        collectprocessed.checked = true
        for (i = 0; i < collectDateBox.length; i++) {
            if (collectDateBox[i].children[9].classList.contains("unprocessed")) {
                collectDateBox[i].classList.add("tRdisplayNone")
            }else{
                collectDateBox[i].classList.remove("tRdisplayNone")
            }
        };
    }
}

collectprocessed.addEventListener("change", optionProcessed)

function optionProcessed() {
    if (this.checked && collectUnprocessed.checked) {
        for (i = 0; i < collectDateBox.length; i++) {
            if (collectDateBox[i].children[9].classList.contains("processed")) {
                collectDateBox[i].classList.remove("tRdisplayNone")
            }
        };
    } else if (!this.checked && collectUnprocessed.checked) {
        for (i = 0; i < collectDateBox.length; i++) {
            if (collectDateBox[i].children[9].classList.contains("processed")) {
                collectDateBox[i].classList.add("tRdisplayNone")
            }
        };
    } else if (!this.checked && !collectUnprocessed.checked) {
        collectUnprocessed.checked = true
        for (i = 0; i < collectDateBox.length; i++) {
            if (collectDateBox[i].children[9].classList.contains("processed")) {
                collectDateBox[i].classList.add("tRdisplayNone")
            }else{
                collectDateBox[i].classList.remove("tRdisplayNone")
            }
        };
    }
}