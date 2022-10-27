const dayTotal = document.querySelectorAll(".dayTotal")
const depositDateTable = document.querySelectorAll(".depositDateTable")

window.onload = function () {
    calcTotal()
}

function calcTotal() {
    for (i = 0; i < depositDateTable.length; i++) {
        dayTotal[i].children[6].innerText = 0
        dayTotal[i].children[7].innerText = 0
        dayTotal[i].children[8].innerText = 0
        for (j = 0; j < depositDateTable[i].children[1].children.length - 1; j++) {
            if (!depositDateTable[i].children[1].children[j].classList.contains("tRdisplayNone")) {
                dayTotal[i].children[6].innerText =
                    parseInt(dayTotal[i].children[6].innerText.replace(/\,/g, ""))
                    + parseInt(depositDateTable[i].children[1].children[j].children[6].innerText.replace(/\,/g, ""))
                dayTotal[i].children[7].innerText =
                    parseInt(dayTotal[i].children[7].innerText.replace(/\,/g, ""))
                    + parseInt(depositDateTable[i].children[1].children[j].children[7].innerText.replace(/\,/g, ""))
                dayTotal[i].children[8].innerText =
                    parseInt(dayTotal[i].children[8].innerText.replace(/\,/g, ""))
                    + parseInt(depositDateTable[i].children[1].children[j].children[8].innerText.replace(/\,/g, ""))
            }
        };
        dayTotal[i].children[9].innerText = `합계 ${
            parseInt(dayTotal[i].children[6].innerText.replace(/\,/g, ""))
            + parseInt(dayTotal[i].children[7].innerText.replace(/\,/g, ""))
        }`.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        dayTotal[i].children[6].innerText = dayTotal[i].children[6].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        dayTotal[i].children[7].innerText = dayTotal[i].children[7].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        dayTotal[i].children[8].innerText = dayTotal[i].children[8].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    };
}