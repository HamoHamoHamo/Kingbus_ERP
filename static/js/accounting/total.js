const collectDateBox = document.querySelectorAll(".collectDateBox")
const selectTotal = document.querySelector(".selectTotal")
const tatalCount = document.querySelector(".tatalCount")
const downPayment = document.querySelector(".downPayment")
const tatalPrice = document.querySelector(".tatalPrice")
const tatalSupplyPrice = document.querySelector(".tatalSupplyPrice")
const tatalVat = document.querySelector(".tatalVat")
const tatalCollect = document.querySelector(".tatalCollect")
const uaccountsReceivablen = document.querySelector(".uaccountsReceivablen")
const depositState = document.querySelector(".depositState")
const SupplyPrice = document.querySelectorAll(".SupplyPrice")
const Vat = document.querySelectorAll(".Vat")
const Collect = document.querySelectorAll(".Collect")

function calcTotal(unprocessed, processed) {
    let calcArr = []
    if(unprocessed && processed){
        for(i=0; i<collectDateBox.length; i++){
            calcArr.push(collectDateBox[i])
        }
    }else if(unprocessed && !processed){
        for(i=0; i<collectDateBox.length; i++){
            if(collectDateBox[i].children[12].innerText === "미수금"){
                calcArr.push(collectDateBox[i])
            }
        }
    }else if(!unprocessed && processed){
        for(i=0; i<collectDateBox.length; i++){
            if(collectDateBox[i].children[12].innerText === "완료"){
                calcArr.push(collectDateBox[i])
            }
        }
    }

    let downPaymentPrice = 0
    let tatalSupply = 0
    let tatalVatPrice = 0
    let uaccountsReceivablenPrice = 0
    for (i = 0; i < calcArr.length; i++){
        downPaymentPrice = downPaymentPrice + parseInt(calcArr[i].children[6].innerText)
        tatalSupply = tatalSupply + parseInt(calcArr[i].children[8].innerText)
        tatalVatPrice = tatalVatPrice + parseInt(calcArr[i].children[9].innerText)
        uaccountsReceivablenPrice = uaccountsReceivablenPrice + parseInt(calcArr[i].children[13].innerText)
    };
    tatalCount.innerText = `건수 ${calcArr.length}`
    downPayment.innerText = downPaymentPrice
    tatalSupplyPrice.innerText = tatalSupply
    tatalVat.innerText = tatalVatPrice
    tatalCollect.innerText = tatalSupply + tatalVatPrice
    uaccountsReceivablen.innerText = uaccountsReceivablenPrice

    if(uaccountsReceivablenPrice !== 0){
        depositState.innerText = "미수금"
        depositState.style.color = "red"
    }else{
        depositState.innerText = "완료"
        depositState.style.color = "black"
    }

    downPayment.innerText = downPayment.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    tatalSupplyPrice.innerText = tatalSupplyPrice.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    tatalVat.innerText = tatalVat.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    tatalCollect.innerText = tatalCollect.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    uaccountsReceivablen.innerText = uaccountsReceivablen.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");

    
    for (i = 0; i < collectDateBox.length; i++){
        collectDateBox[i].children[6].innerText = collectDateBox[i].children[6].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        collectDateBox[i].children[8].innerText = collectDateBox[i].children[8].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        collectDateBox[i].children[9].innerText = collectDateBox[i].children[9].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        collectDateBox[i].children[10].innerText = collectDateBox[i].children[10].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        collectDateBox[i].children[13].innerText = collectDateBox[i].children[13].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    }
}