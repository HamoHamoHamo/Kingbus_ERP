const depositDateTable = document.querySelectorAll(".depositDateTable")


function calcTotal() {
    const dayTotal = document.querySelectorAll(".dayTotal")

    totalCalculate(0, 0)

    function totalCalculate(totalCount, startTarget) {
        let commission = 0
        let deposit = 0
        let processed = 0
        for (i = startTarget; i < depositTbody.children.length; i++) {
            if (depositTbody.children[i].style.display == "table-row") {
                commission = commission + parseInt(depositTbody.children[i].children[6].innerText)
                deposit = deposit + parseInt(depositTbody.children[i].children[7].innerText)
                processed = processed + parseInt(depositTbody.children[i].children[8].innerText)
            }
            if (depositTbody.children[i] === dayTotal[totalCount]) {

                dayTotal[totalCount].children[1].innerText = commission
                dayTotal[totalCount].children[2].innerText = deposit
                dayTotal[totalCount].children[3].innerText = processed
                dayTotal[totalCount].children[4].innerText = commission + deposit

                startTarget = i

                totalCount++
                return totalCalculate(totalCount, startTarget)
            }
        };

        for (i = 0; i < dayTotal.length; i++) {
            dayTotal[i].children[1].innerText = dayTotal[i].children[1].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
            dayTotal[i].children[2].innerText = dayTotal[i].children[2].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
            dayTotal[i].children[3].innerText = dayTotal[i].children[3].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        };
    }

    for (i = 0; i < depositCell.length; i++){
        depositCell[i].children[6].innerText = depositCell[i].children[6].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        depositCell[i].children[7].innerText = depositCell[i].children[7].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        depositCell[i].children[8].innerText = depositCell[i].children[8].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    };

}