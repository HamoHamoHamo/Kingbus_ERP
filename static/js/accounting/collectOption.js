const collectUnprocessed = document.querySelector("#collectUnprocessed")
const collectprocessed = document.querySelector("#collectprocessed")


collectUnprocessed.addEventListener("change", visibleUnprocessed)

function visibleUnprocessed() {
    if (collectUnprocessed.checked && collectprocessed.checked) {
        for (i = 0; i < collectDateBox.length; i++){
            collectDateBox[i].classList.remove("tRdisplayNone")
        };
    } else if (!collectUnprocessed.checked && collectprocessed.checked) {
        for (i = 0; i < collectDateBox.length; i++){
            if(collectDateBox[i].children[13].classList.contains("unprocessed")){
                collectDateBox[i].classList.add("tRdisplayNone")
            }else{
                collectDateBox[i].classList.remove("tRdisplayNone")
            }
        };
    } else {
        collectprocessed.checked = true
        for (i = 0; i < collectDateBox.length; i++){
            if(collectDateBox[i].children[13].classList.contains("unprocessed")){
                collectDateBox[i].classList.remove("tRdisplayNone")
            }else{
                collectDateBox[i].classList.add("tRdisplayNone")
            }
        };
    }
    calcTotal(collectUnprocessed.checked, collectprocessed.checked)
}


collectprocessed.addEventListener("change", visibleProcessed)

function visibleProcessed() {
    if (collectUnprocessed.checked && collectprocessed.checked) {
        for (i = 0; i < collectDateBox.length; i++){
            collectDateBox[i].classList.remove("tRdisplayNone")
        };
    } else if (!collectprocessed.checked && collectUnprocessed.checked) {
        for (i = 0; i < collectDateBox.length; i++){
            if(collectDateBox[i].children[13].classList.contains("processed")){
                collectDateBox[i].classList.add("tRdisplayNone")
            }else{
                collectDateBox[i].classList.remove("tRdisplayNone")
            }
        };
    } else {
        collectUnprocessed.checked = true
        for (i = 0; i < collectDateBox.length; i++){
            if(collectDateBox[i].children[13].classList.contains("processed")){
                collectDateBox[i].classList.remove("tRdisplayNone")
            }else{
                collectDateBox[i].classList.add("tRdisplayNone")
            }
        };
    }
    calcTotal(collectUnprocessed.checked, collectprocessed.checked)
}

calcTotal(collectUnprocessed.checked, collectprocessed.checked)