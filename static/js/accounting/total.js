const collectDateBox = document.querySelectorAll(".collectDateBox")
const selectTotal = document.querySelector(".selectTotal")
const tatalCount = document.querySelector(".tatalCount")
const tatalPrice = document.querySelector(".tatalPrice")
const tatalSupplyPrice = document.querySelector(".tatalSupplyPrice")
const tatalVat = document.querySelector(".tatalVat")
const tatalCollect = document.querySelector(".tatalCollect")
const SupplyPrice = document.querySelectorAll(".SupplyPrice")
const Vat = document.querySelectorAll(".Vat")
const Collect = document.querySelectorAll(".Collect")

window.onload = function () {
    calcTotal()
}

function calcTotal() {
    for (i = 0; i < Collect.length; i++){ 
        Collect[i].innerText = parseInt(SupplyPrice[i].innerText.replace(/\,/g,"")) + parseInt(Vat[i].innerText.replace(/\,/g,""))
        Collect[i].innerText = Collect[i].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    };
    tatalCount.innerText = 0
    tatalPrice.innerText = 0
    tatalSupplyPrice.innerText = 0
    tatalVat.innerText = 0
    tatalCollect.innerText = 0
    for (i = 0; i < collectDateBox.length; i++){
        if (depositDateTable[i].children[1].children[j].style.display !== "none") {
            tatalCount.innerText = parseInt(tatalCount.innerText) + 1
            tatalPrice.innerText = parseInt(tatalPrice.innerText) + parseInt(collectDateBox[i].children[6].innerText.replace(/\,/g, ""))
            tatalSupplyPrice.innerText = parseInt(tatalSupplyPrice.innerText) + parseInt(collectDateBox[i].children[8].innerText.replace(/\,/g, ""))
            tatalVat.innerText = parseInt(tatalVat.innerText) + parseInt(collectDateBox[i].children[9].innerText.replace(/\,/g, ""))
            tatalCollect.innerText = parseInt(tatalCollect.innerText) + parseInt(collectDateBox[i].children[10].innerText.replace(/\,/g, ""))
        }
    };
    tatalPrice.innerText = tatalPrice.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    tatalSupplyPrice.innerText = tatalSupplyPrice.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    tatalVat.innerText = tatalVat.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    tatalCollect.innerText = tatalCollect.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}