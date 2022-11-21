const amountProcessed = document.querySelectorAll(".depositCell td:nth-child(9)")
const amountProcessedCloseBtn = document.querySelector(".amountProcessedCloseBtn")
const amountProcessedTitle = document.querySelector(".amountProcessedTitle")
const amountProcessedTbody = document.querySelector(".amountProcessedForm tbody")

for (i = 0; i < amountProcessed.length; i++) {
    amountProcessed[i].addEventListener("click", openPopup)
};

function openPopup(event) {
    event.stopPropagation()
    popupAreaModules[1].style.display = "block"
    amountProcessedTitle.innerText = `[${this.parentNode.children[1].innerText}] 처리내역`

    amountProcessedTbody.innerText = ""

    let findChit = 0

    for (i = 0; i < depositCell.length; i++) {
        if (this.parentNode === depositCell[i])
            findChit = i
    };

    for (i = 0; i < collectList[findChit].length; i++) {
        const apTr = document.createElement("tr")
        apTr.setAttribute("class", "table-list_body-tr")
        amountProcessedTbody.appendChild(apTr)

        const apTd1 = document.createElement("td")
        apTd1.setAttribute("class", "table-list_body-tr_td")
        apTd1.innerText = i + 1
        apTr.appendChild(apTd1)

        const apTd2 = document.createElement("td")
        apTd2.setAttribute("class", "table-list_body-tr_td")
        apTd2.innerText = collectList[findChit][i].type
        apTr.appendChild(apTd2)

        const apTd3 = document.createElement("td")
        apTd3.setAttribute("class", "table-list_body-tr_td")
        apTd3.setAttribute("title", collectList[findChit][i].name)
        apTr.appendChild(apTd3)

        let departureName = collectList[findChit][i].name.split(" ▶")[0]
        let arrivalName = collectList[findChit][i].name.split("▶ ")[1]
        
        const name1 = document.createElement("div")
        if(collectList[findChit][i].type ==="일반"){
            if(departureName.length >= 26){
                name1.innerText = `${departureName.substr(0,24)}... ▶`
            }else{
                name1.innerText = departureName
            }
            apTd3.appendChild(name1)
            
            const name2 = document.createElement("div")
            if(arrivalName.length >= 28){
                name2.innerText = `${arrivalName.substr(0,26)}...`
            }else{
                name2.innerText = arrivalName
            }
            apTd3.appendChild(name2)
        }else{
            if(collectList[findChit][i].name.length >= 28){
                name1.innerText = `${collectList[findChit][i].name.substr(0,26)}...`
            }else{
                name1.innerText = collectList[findChit][i].name
            }
            apTd3.appendChild(name1)
        }

        const apTd4 = document.createElement("td")
        apTd4.setAttribute("class", "table-list_body-tr_td")
        apTr.appendChild(apTd4)

        if (collectList[findChit][i].date1.substr(0, 10) === collectList[findChit][i].date2.substr(0, 10)) {
            const dateDiv1 = document.createElement("div")
            dateDiv1.innerText = collectList[findChit][i].date1.substr(0, 10)
            apTd4.appendChild(dateDiv1)

            const dateDiv2 = document.createElement("div")
            dateDiv2.innerText = `${collectList[findChit][i].date1.substr(11, )} ~ ${collectList[findChit][i].date2.substr(11, )}`
            apTd4.appendChild(dateDiv2)
        } else {
            const dateDiv1 = document.createElement("div")
            dateDiv1.innerText = collectList[findChit][i].date1
            apTd4.appendChild(dateDiv1)

            const dateDiv2 = document.createElement("div")
            dateDiv2.innerText = collectList[findChit][i].date1
            apTd4.appendChild(dateDiv2)
        }

        const apTd5 = document.createElement("td")
        apTd5.setAttribute("class", "table-list_body-tr_td")
        apTd5.innerText = collectList[findChit][i].price
        apTr.appendChild(apTd5)

        const apTd6 = document.createElement("td")
        apTd6.setAttribute("class", "table-list_body-tr_td")
        apTd6.innerText = collectList[findChit][i].used_price
        apTr.appendChild(apTd6)
    }
    const apTr = document.querySelectorAll(".amountProcessedForm tbody .table-list_body-tr")
    APaddComma(apTr)
}

popupBgModules[1].addEventListener("click", closePopup)
SidemenuUseClose.addEventListener("click", closePopup)
amountProcessedCloseBtn.addEventListener("click", closePopup)

function closePopup() {
    popupAreaModules[1].style.display = "none"
}



function APaddComma(apTr){
    for (i = 0; i < apTr.length; i++){
        apTr[i].children[4].innerText = apTr[i].children[4].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        apTr[i].children[5].innerText = apTr[i].children[5].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    };    
}