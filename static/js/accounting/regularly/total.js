const tatalCount = document.querySelector(".tatalCount")
const tatalPrice = document.querySelector(".tatalPrice")
const tatalSupplyPrice = document.querySelector(".tatalSupplyPrice")
const tatalVat = document.querySelector(".tatalVat")
const tatalAdd = document.querySelector(".tatalAdd")
const tatalCollect = document.querySelector(".tatalCollect")
const totalDepositState = document.querySelector(".totalDepositState")
const totalAccountsReceivable = document.querySelector(".totalAccountsReceivable")


function calculate() {

    let price = 0
    let supplyPrice = 0
    let vat = 0
    let add = 0
    let accountsReceivable = 0
    for (i = 0; i < collectDateBox.length; i++) {
        if (!collectDateBox[i].classList.contains("tRdisplayNone")) {
            price = price + parseInt(collectDateBox[i].children[3].innerText.replace(/\,/g, ""))
            supplyPrice = supplyPrice + parseInt(collectDateBox[i].children[4].innerText.replace(/\,/g, ""))
            vat = vat + parseInt(collectDateBox[i].children[5].innerText.replace(/\,/g, ""))
            add = add + parseInt(collectDateBox[i].children[6].innerText.replace(/\,/g, ""))
            accountsReceivable = accountsReceivable + parseInt(collectDateBox[i].children[10].innerText.replace(/\,/g, ""))
        }
    };
    tatalCount.innerText = `그룹 ${collectDateBox.length}`
    tatalPrice.innerText = price
    tatalSupplyPrice.innerText = supplyPrice
    tatalVat.innerText = vat
    tatalAdd.innerText = add
    tatalCollect.innerText = supplyPrice + vat + add
    totalDepositState.innerText = accountsReceivable === 0 ? "완료" : "미수금";
    totalAccountsReceivable.innerText = accountsReceivable

    totalDepositState.innerText === "미수금" ? totalDepositState.style.color = "red" : null;

    tatalPrice.innerText = tatalPrice.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    tatalSupplyPrice.innerText = tatalSupplyPrice.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    tatalVat.innerText = tatalVat.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    tatalAdd.innerText = tatalAdd.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    tatalCollect.innerText = tatalCollect.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    totalAccountsReceivable.innerText = totalAccountsReceivable.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}

calculate();