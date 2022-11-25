const searchBox = document.querySelector(".search-Form_input")
const searchBtn = document.querySelector(".search-Form_search-btn")
const totalBox = document.querySelectorAll(".totalBox")

searchBtn.addEventListener("click", filterlingOrder)

function filterlingOrder(){
    console.log(orderListBox);
    for (i = 0; i < orderListBox.length-1; i++){
        orderListBox[i].innerText = ""
        totalBox[i].children[1].innerText = ""
    };
    drawOrder(searchBox.value)
    
    const orderListCell = document.querySelectorAll(".orderListCell")

    for (i = 0; i < orderListCell.length; i++) {
        orderListCell[i].addEventListener("click", locationOrder)
    };
}

document.addEventListener("keydown", saveKeyPress)

function saveKeyPress(e) {
    if (e.keyCode === 13) {
        filterlingOrder()
    }
}
