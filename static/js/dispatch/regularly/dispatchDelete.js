const RouteList = document.querySelector(".RouteList")
const dispatchDeletBtn = document.querySelector(".dispatchDeletBtn")

dispatchDeletBtn.addEventListener("click", deleteDispatch)

function deleteDispatch(){
    RouteList.action = "regularly/connect/delete"
    let bus = ""
    let driver = ""
    for (i = 0; i < RouteListHBodyTr.length; i++){
        if(RouteListHBodyTr[i].children[0].children[0].checked){
            bus = RouteListHBodyTr[i].children[4].children[1].value
            let selecting = RouteListHBodyTr[i].children[5].children[0]
            let outsorcingSelecting = RouteListHBodyTr[i].children[6].children[0]
            if(selecting.options[selecting.selectedIndex].value !== "" && outsorcingSelecting.options[outsorcingSelecting.selectedIndex].value === ""){
                driver = selecting.options[selecting.selectedIndex].value
            }else if(selecting.options[selecting.selectedIndex].value === "" && outsorcingSelecting.options[outsorcingSelecting.selectedIndex].value !== ""){
                driver = outsorcingSelecting.options[selecting.selectedIndex].value
            }else if(selecting.options[selecting.selectedIndex].value === "" && outsorcingSelecting.options[outsorcingSelecting.selectedIndex].value === ""){
                driver = ""
            }
        }
    };
    if(bus === "" && driver === ""){
        alert("삭제할 배차가 없습니다.")
    }else{
        RouteList.submit();
    }
}