const printTableCell = document.querySelectorAll(".printTableCell")
const printBox = document.querySelector(".print")
const printTable = document.querySelector(".printTable")

function resize() {
    for (i = 0; i < printTableCell.length; i++) {
        let heightArr = []
        for (j = 0; j < printTableCell[i].children.length; j++) {
            heightArr.push(printTableCell[i].children[j].offsetHeight - 10)
            heightArr.sort(function (a, b) {
                return b - a;
            })
        };

        for (j = 0; j < printTableCell[i].children.length; j++) {
            printTableCell[i].children[j].style.height = `${heightArr[0] * 0.1}rem`
        }
    };
}

function nextPageFirst() {
    let targeHeight = (51.2 + 44.797) / 3.78 + 15
    for (i = 0; i < printTableCell.length; i++) {
        targeHeight = targeHeight + printTableCell[i].offsetHeight / 3.78
        if (targeHeight > 400) {
            targeHeight = targeHeight - printTableCell[i].offsetHeight / 3.78
            printTableCell[i - 1].style.marginBottom = `${445 - targeHeight}mm`
            printTableCell[i - 1].style.position = "relative"
            const pageCount = document.createElement("div")
            pageCount.setAttribute("class", "pageNumber")
            pageCount.setAttribute("style", `top : ${printTableCell[i - 1].offsetHeight * 0.378}mm`)
            printTableCell[i - 1].appendChild(pageCount)
            printTableCell[i].style.borderTop = `0.1rem solid black`
            return nextPage(i)
        }
    };
}

function nextPage(rocation) {
    let targeHeight = 0
    for (i = rocation; i < printTableCell.length; i++) {
        targeHeight = targeHeight + printTableCell[i].offsetHeight / 3.78
        if (targeHeight > 385) {
            targeHeight = targeHeight - printTableCell[i].offsetHeight / 3.78
            printTableCell[i - 1].style.marginBottom = `${430 - targeHeight}mm`
            printTableCell[i - 1].style.position = "relative"
            const pageCount = document.createElement("div")
            pageCount.setAttribute("class", "pageNumber")
            pageCount.setAttribute("style", `top : ${printTableCell[i - 1].offsetHeight * 0.378}mm`)
            printTableCell[i - 1].appendChild(pageCount)
            printTableCell[i].style.borderTop = `0.1rem solid black`
            rocation = i
            return nextPage(rocation)
        }

        if (i === printTableCell.length - 1) {
            let lastHeight = 0
            for (i = rocation; i < printTableCell.length; i++) {
                lastHeight = lastHeight + printTableCell[i].offsetHeight / 3.78
            };
            printTableCell[printTableCell.length - 1].style.position = "relative"
            const pageCount = document.createElement("div")
            pageCount.setAttribute("class", "pageNumber")
            pageCount.setAttribute("style", `top : ${400 - lastHeight}mm`)
            printTableCell[printTableCell.length - 1].appendChild(pageCount)
        }
    };
}

function addPageNumber() {
    const pageNumber = document.querySelectorAll(".pageNumber")

    for (i = 0; i < pageNumber.length; i++) {
        pageNumber[i].innerText = `${i + 1} / ${pageNumber.length}`
    };
}

resize();
nextPageFirst();
addPageNumber();