const RouteListScroll = document.querySelector(".RouteListScroll")
const route = document.querySelectorAll(".RouteListBodyTr")
const inputSelect = document.querySelector(".inputSelect")
const routeListsearch = document.querySelector("#routeListsearch")
const amountComma = document.querySelectorAll(".amountComma")
const pricePopupArea = document.querySelectorAll(".pricePopupArea")


window.onload = function () {

    let parms = new URLSearchParams(location.search)

    addComma()
    
    savePrice0 =  pricePopupArea[0].innerText.replace(/\,/g,"")
    savePrice1 =  pricePopupArea[1].innerText.replace(/\,/g,"")

    const RouteListBodyTr = document.querySelectorAll(".RouteListBodyTr")
    RouteListScroll.scrollTop = parms.get("height")


    if (!parms.has("id")) {
        amountComma[0].value = amountComma[0].value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        amountComma[1].value = amountComma[1].value.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    }else{
        amountComma[0].innerText = amountComma[0].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        amountComma[1].innerText = amountComma[1].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    }

    if (parms.has("id")) {
        for (i = 0; i < RouteListBodyTr.length; i++) {
            if (RouteListBodyTr[i].classList[1] == parms.get("id")) {
                RouteListBodyTr[i].style.backgroundColor = "#CDCDCE"
            }
        };
    }
    if (parseInt(parms.get("close"))) {
        groupClose()
    }
    if (parms.has("group")) {
        const groupListItem = document.querySelectorAll(".groupListItem")
        for (i = 0; i < groupListItem.length; i++) {
            if (groupListItem[i].classList[1] == parms.get("group")) {
                groupListItem[i].style.backgroundColor = "#CDCDCE"
            }
        };
        for (i = 0; i < inputSelect.children.length; i++) {
            if (inputSelect.children[i].value === parms.get("group")) {
                return inputSelect.children[i].selected = true
            }
        };
    }
    if (parms.has("search")) {
        routeListsearch.value = parms.get("search")
    }
}