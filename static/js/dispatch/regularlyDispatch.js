const routeList = document.querySelectorAll(".listTable tbody tr")
const routeListBus = document.querySelectorAll(".listTable tbody td:nth-child(3)")
const orderDriver = document.querySelectorAll(".orderDriver")
const orderSpareDriver = document.querySelectorAll(".orderSpareDriver")


window.onload = function () {
    dispatchCheck()
    inputToDay()
    useDriver()
}

// 배차 가능 노선 표시
function dispatchCheck() {
    if (window.location.search.substr(0, 3) == "?id") {
        for (i = 0; i < routeList.length; i++) {
            if (routeList[i].classList[0] == window.location.search.split("=")[1]) {
                routeList[i].classList.add("checkBus")
                routeList[i].children[2].style.backgroundColor = "#0069D9"
                routeList[i].children[3].style.backgroundColor = "#0069D9"
                routeList[i].children[4].style.backgroundColor = "#0069D9"
            }
        }
    }
}



// 운전원, 용역 보이기
function useDriver(){
    for(i=0; i<routeList.length; i++){
        if(window.location.search.split("id=")[1] == routeList[i].classList[0] && routeListBus[i].innerText !== ""){
            orderDriver[i].style.display = "block"
            orderSpareDriver[i].style.display = "block"
        }
    }    
}




// 운전원, 용역 변경시 새로고침 막기
for(i=0; i<orderDriver.length; i++){
    orderDriver[i].addEventListener("click", stopLink)
    orderSpareDriver[i].addEventListener("click", stopLink)
}

function stopLink(e){
    e.stopPropagation()
}