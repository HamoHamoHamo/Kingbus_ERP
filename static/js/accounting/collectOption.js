const collectUnprocessed = document.querySelector("#collectUnprocessed")
const collectprocessed = document.querySelector("#collectprocessed")


collectUnprocessed.addEventListener("change", visibleCheck)
collectprocessed.addEventListener("change", visibleCheck)

function visibleCheck(e) {
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
    } else if (collectUnprocessed.checked && !collectprocessed.checked) {
        for (i = 0; i < collectDateBox.length; i++){
            if(collectDateBox[i].children[13].classList.contains("processed")){
                collectDateBox[i].classList.add("tRdisplayNone")
            }else{
                collectDateBox[i].classList.remove("tRdisplayNone")
            }
        };
    } else {
        
        if (e.target == collectUnprocessed) {
            collectprocessed.checked = true
            for (i = 0; i < collectDateBox.length; i++){
                if(collectDateBox[i].children[13].classList.contains("processed")){
                    collectDateBox[i].classList.remove("tRdisplayNone")
                }else{
                    collectDateBox[i].classList.add("tRdisplayNone")
                }
            };
        }
        else if (e.target == collectprocessed) {
            collectUnprocessed.checked = true
            for (i = 0; i < collectDateBox.length; i++){
                if(collectDateBox[i].children[13].classList.contains("unprocessed")){
                    collectDateBox[i].classList.remove("tRdisplayNone")
                }else{
                    collectDateBox[i].classList.add("tRdisplayNone")
                }
            };
        }
    }
    
    routeRadioAll.checked = false
    for (i = 0; i < routeRadio.length; i++) {
        routeRadio[i].checked = false
    };
    calcTotal(collectUnprocessed.checked, collectprocessed.checked)
}



calcTotal(collectUnprocessed.checked, collectprocessed.checked)