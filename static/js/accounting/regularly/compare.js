const comparePopup = document.querySelector(".comparePopup")
const popupBgModulesCompare = document.querySelector(".popupBgModulesCompare")
const compareCloseBtn = document.querySelector(".compareCloseBtn")
const compareTable = document.querySelector(".compareTableScroll tbody")
const compareCount = document.querySelector(".compareCount")
const comparePrice = document.querySelector(".comparePrice")
const compareVat = document.querySelector(".compareVat")

for (i = 0; i < collectDateBox.length; i++) {
    collectDateBox[i].children[3].addEventListener("click", openComparePopup)
};

function openComparePopup() {
    comparePopup.style.display = "block"

    let compareData = {
        date1: `20${this.parentNode.children[2].innerText.substr(0, 8).replace(/\//g, "-")}`,
        date2: `20${this.parentNode.children[2].innerText.substr(11, 8).replace(/\//g, "-")}`,
        group_id: this.parentNode.children[0].children[0].value
    }
    $.ajax({
        url: "/accounting/regularly/load",
        method: "POST",
        data: JSON.stringify(compareData),
        datatype: 'json',
        success: function (result) {
            if (result.status) {
                compareTable.innerText = ""
                for (i = 0; i < result.dataList.length; i++) {
                    const compareTr = document.createElement("tr")
                    compareTr.setAttribute("class", "table-list_body-tr")
                    compareTable.appendChild(compareTr)

                    const compareBox1 = document.createElement("td")
                    compareBox1.setAttribute("class", "table-list_body-tr_td")
                    compareTr.appendChild(compareBox1)

                    if (result.dataList[i].duration.substr(0, 7) === result.dataList[i].duration.substr(13, 7)) {
                        const compareDiv = document.createElement("div")
                        compareDiv.setAttribute("class", "displayDivCenter")
                        compareBox1.appendChild(compareDiv)

                        const compareSpan0 = document.createElement("span")
                        compareSpan0.innerText = result.dataList[i].duration.substr(0, 7)
                        compareDiv.appendChild(compareSpan0)

                        const compareSpan1 = document.createElement("span")
                        compareSpan1.innerText = `${result.dataList[i].duration.substr(8, 2)}~${result.dataList[i].duration.substr(21, 2)}`
                        compareDiv.appendChild(compareSpan1)
                    } else {
                        const compareDiv = document.createElement("div")
                        compareDiv.setAttribute("class", "displayDiv")
                        compareBox1.appendChild(compareDiv)

                        const compareSpan0 = document.createElement("span")
                        compareSpan0.innerText = `${result.dataList[i].duration.split("~")[0]}~`
                        compareDiv.appendChild(compareSpan0)

                        const compareSpan1 = document.createElement("span")
                        compareSpan1.innerText = result.dataList[i].duration.split("~ ")[1]
                        compareDiv.appendChild(compareSpan1)
                    }

                    const compareBox2 = document.createElement("td")
                    compareBox2.setAttribute("class", "table-list_body-tr_td")
                    compareBox2.innerText = result.dataList[i].week
                    compareTr.appendChild(compareBox2)

                    const compareBox3 = document.createElement("td")
                    compareBox3.setAttribute("class", "table-list_body-tr_td")
                    compareBox3.innerText = result.dataList[i].type
                    compareTr.appendChild(compareBox3)

                    const compareBox4 = document.createElement("td")
                    compareBox4.setAttribute("class", "table-list_body-tr_td")
                    compareBox4.innerText = result.dataList[i].route
                    compareTr.appendChild(compareBox4)

                    const compareBox5 = document.createElement("td")
                    compareBox5.setAttribute("class", "table-list_body-tr_td")
                    compareBox5.innerText = result.dataList[i].cnt
                    compareTr.appendChild(compareBox5)

                    const compareBox6 = document.createElement("td")
                    compareBox6.setAttribute("class", "table-list_body-tr_td")
                    compareBox6.innerText = result.dataList[i].contract_price
                    compareTr.appendChild(compareBox6)

                    const compareBox7 = document.createElement("td")
                    compareBox7.setAttribute("class", "table-list_body-tr_td")
                    compareBox7.innerText = result.dataList[i].supply_price
                    compareTr.appendChild(compareBox7)

                    const compareBox8 = document.createElement("td")
                    compareBox8.setAttribute("class", "table-list_body-tr_td")
                    compareBox8.innerText = result.dataList[i].VAT
                    compareTr.appendChild(compareBox8)

                };
                const compareItem = document.querySelectorAll(".compareTableScroll tr")
                addComma(compareItem)
                compareTotal(compareItem)
            } else {
                alert("정산목록을 불러오지 못했습니다.")
            }
        },
        error: function (request, error) {
            console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
        },
    });
    
}


popupBgModulesCompare.addEventListener("click", closeComparePopup)
compareCloseBtn.addEventListener("click", closeComparePopup)
SidemenuUseClose.addEventListener("click", closeComparePopup)

function closeComparePopup() {
    comparePopup.style.display = "none"
}


function addComma(compareItem) {
    for (i = 0; i < compareItem.length; i++) {
        console.log(compareItem);
        compareItem[i].children[4].innerText = compareItem[i].children[4].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        compareItem[i].children[5].innerText = compareItem[i].children[5].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        compareItem[i].children[6].innerText = compareItem[i].children[6].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        compareItem[i].children[7].innerText = compareItem[i].children[7].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    };
}


function compareTotal(compareItem) {
    let count = 0
    let price = 0
    let vat = 0
    for (i = 0; i < compareItem.length; i++) {
        count = count + parseInt(compareItem[i].children[4].innerText.replace(/\,/g, ""))
        price = price + parseInt(compareItem[i].children[6].innerText.replace(/\,/g, ""))
        vat = vat + parseInt(compareItem[i].children[7].innerText.replace(/\,/g, ""))
    };
    compareCount.innerText = count
    comparePrice.innerText = price
    compareVat.innerText = vat
    compareCount.innerText = compareCount.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    comparePrice.innerText = comparePrice.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    compareVat.innerText = compareVat.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}