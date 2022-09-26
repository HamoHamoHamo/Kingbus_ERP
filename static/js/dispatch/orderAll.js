window.onload = function () {
    inputToDay()
    matchHeight()
    drawSchdule()
    DispatcBusFilter()
    notPairFilter()
    addCommaList()
    changeVAT()
    pageLoadAddComma()
    listHeight()
}



let inputStartTime = ""
let inputEndTime = ""
let params = new URLSearchParams(document.location.search)