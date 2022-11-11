const selectTotal = document.querySelector(".checkTotalTable tr")

function totalSelecting(selectArr) {
    let commission = 0
    let deposit = 0
    let process = 0
    let total = 0
    for (i = 0; i < selectArr.length; i++){
        commission = commission + parseInt(depositCell[selectArr[i]].children[6].innerText.replace(/\,/g, ""))
        deposit = deposit + parseInt(depositCell[selectArr[i]].children[7].innerText.replace(/\,/g, ""))
        process = process + parseInt(depositCell[selectArr[i]].children[8].innerText.replace(/\,/g, ""))
    };
    total = commission + deposit
    selectTotal.children[1].innerText = commission
    selectTotal.children[1].innerText = selectTotal.children[1].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")
    selectTotal.children[2].innerText = deposit
    selectTotal.children[2].innerText = selectTotal.children[2].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")
    selectTotal.children[3].innerText = process
    selectTotal.children[3].innerText = selectTotal.children[3].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")
    selectTotal.children[4].innerText = total
    selectTotal.children[4].innerText = `합계 ${selectTotal.children[4].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")}`
}
