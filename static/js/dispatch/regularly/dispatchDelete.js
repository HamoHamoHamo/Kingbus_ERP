const RouteList = document.querySelector(".RouteList")
const dispatchDeletBtn = document.querySelector(".dispatchDeletBtn")

dispatchDeletBtn.addEventListener("click", deleteDispatch)

function deleteDispatch(){
    RouteList.action = "regularly/connect/delete"
    RouteList.submit()
}