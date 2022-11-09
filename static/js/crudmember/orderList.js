const orderListBox = document.querySelectorAll(".orderListBox")

function drawOrder(filter) {
    if(filter === undefined){
        for (i = 0; i < orderListBox.length - 1; i++) {
            for (j = 0; j < changeOrderList[i].length; j++) {
                const orderListCell = document.createElement("div")
                orderListCell.setAttribute("class", "orderListCell")
                orderListBox[i].appendChild(orderListCell)
    
                const orderListCellCustomer = document.createElement("span")
                orderListCellCustomer.innerText = changeOrderList[i][j].customer
                orderListCell.appendChild(orderListCellCustomer)
    
                const orderListCellCnt = document.createElement("span")
                orderListCellCnt.innerText = changeOrderList[i][j].cnt
                orderListCell.appendChild(orderListCellCnt)
            };
            orderListBox[i].parentNode.children[1].children[1].innerText = changeOrderList[i].length
        };
    }else{
        for (i = 0; i < orderListBox.length - 1; i++) {
            for (j = 0; j < changeOrderList[i].length; j++) {
                if(changeOrderList[i][j].customer.includes(filter)){
                    const orderListCell = document.createElement("div")
                    orderListCell.setAttribute("class", "orderListCell")
                    orderListBox[i].appendChild(orderListCell)
        
                    const orderListCellCustomer = document.createElement("span")
                    orderListCellCustomer.innerText = changeOrderList[i][j].customer
                    orderListCell.appendChild(orderListCellCustomer)
        
                    const orderListCellCnt = document.createElement("span")
                    orderListCellCnt.innerText = changeOrderList[i][j].cnt
                    orderListCell.appendChild(orderListCellCnt)
                }
            };
                let orderCount = 0;
            for (j = 0; j < changeOrderList[i].length; j++) {
                if(changeOrderList[i][j].customer.includes(filter)){
                    orderCount++
                }
                orderListBox[i].parentNode.children[1].children[1].innerText = orderCount
            }
        };
    }
}