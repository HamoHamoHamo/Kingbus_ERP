const printTableCell = document.querySelectorAll(".printTableCell")

window.onload = function () {
    let heightArr = []
    let higher = ""
    for (i = 0; i < printTableCell.length; i++) {
        printTableCell[i].children[5].innerText = printTableCell[i].children[5].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        printTableCell[i].children[6].innerText = printTableCell[i].children[6].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        printTableCell[i].children[11].innerText = printTableCell[i].children[11].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        printTableCell[i].children[12].innerText = printTableCell[i].children[12].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        for (j = 0; j < printTableCell[i].children.length; j++) {
            heightArr.push(printTableCell[i].children[j].offsetHeight)
        }
        higher = Math.max.apply(null, heightArr)
        for (j = 0; j < printTableCell[i].children.length; j++) {
            printTableCell[i].children[j].style.height = `${(higher - 1) * 0.1}rem`
        }
    }
    let height = 1560
    for (i = 0; i < printTableCell.length; i++) {
        if (printTableCell[i].offsetTop + printTableCell[i].clientHeight > height) {
            printTableCell[i].style.borderTop = "0.1rem solid black"
            printTableCell[i].style.marginTop = `${(height - printTableCell[i].offsetTop + 30)*0.1}rem`
            height = height + 1560
        }
    }
}