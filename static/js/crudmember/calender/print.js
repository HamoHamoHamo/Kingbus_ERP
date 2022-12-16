const printRoute = document.querySelector(".print_route")
const printBus = document.querySelector(".print_bus")

printRoute.addEventListener("click", () => openDispatchPrint("route"))
printBus.addEventListener("click", () => openDispatchPrint("bus"))

function openDispatchPrint(type) {
    let printDay = ""
    let notSelecting = false
    for (i = 0; i < calenderDataBox.length; i++) {
        if (calenderDataBox[i].classList.contains("selecting")) {
            printDay = calenderDataBox[i].children[0].children[0].innerText
            if (printDay <= 9) {
                printDay = `0${printDay}`
            }
            notSelecting = true
        }
    };
    if (!notSelecting) {
        return alert("프린트할 날짜를 선택해 주세요")
    }
    let printtDate = `${calenderDate.innerText.substr(0, 4)}-${calenderDate.innerText.substr(6, 2)}-${printDay}`
    
    if (type === "route"){
        window.open(`dispatch/print/line?date=${printtDate}`, "노선별", "width=1200, height=640")
    }else{
        console.log("bus");
        window.open(`dispatch/print/dailylist?date=${printtDate}`, "호수별", "width=1200, height=640")
    }
}