const dayTotal = document.querySelectorAll(".dayTotal")
const depositDateTable = document.querySelectorAll(".depositDateTable")

window.onload = function () {
    calcTotal()
}

function calcTotal() {
    for (i = 0; i < depositDateTable.length; i++) {
        dayTotal[i].children[1].innerText = 0
        dayTotal[i].children[2].innerText = 0
        dayTotal[i].children[3].innerText = 0
        for (j = 0; j < depositDateTable[i].children[1].children.length - 1; j++) {
            if (!depositDateTable[i].children[1].children[j].classList.contains("tRdisplayNone")) {
                dayTotal[i].children[1].innerText =
                    parseInt(dayTotal[i].children[1].innerText.replace(/\,/g, ""))
                    + parseInt(depositDateTable[i].children[1].children[j].children[5].innerText.replace(/\,/g, ""))
                dayTotal[i].children[2].innerText =
                    parseInt(dayTotal[i].children[2].innerText.replace(/\,/g, ""))
                    + parseInt(depositDateTable[i].children[1].children[j].children[6].innerText.replace(/\,/g, ""))
            }
        };
        dayTotal[i].children[3].innerText = `합계 ${parseInt(dayTotal[i].children[1].innerText.replace(/\,/g, "")) + parseInt(dayTotal[i].children[2].innerText.replace(/\,/g, ""))}`
        dayTotal[i].children[1].innerText = dayTotal[i].children[1].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        dayTotal[i].children[2].innerText = dayTotal[i].children[2].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        dayTotal[i].children[3].innerText = dayTotal[i].children[3].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    };
}