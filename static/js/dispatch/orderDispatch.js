const orderBus = document.querySelectorAll(".orderDispatchTable tbody td:nth-child(1)")

for(i=0; i<orderBus.length; i++){
    orderBus[i].addEventListener("click", checkOrder)
}

function checkOrder(){
    if(!this.classList.contains("checkOrder")){
        for(i=0; i<orderBus.length; i++){
            orderBus[i].classList.remove("checkOrder")
            orderBus[i].style.backgroundColor = "transparent"
        }
        this.classList.add("checkOrder")
        this.style.backgroundColor = "#0069D9"
    }else{
        this.classList.remove("checkOrder")
        this.style.backgroundColor = "transparent"
    }
}