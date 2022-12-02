const routeCopyBtn = document.querySelector(".routeCopyBtn")
const inputDelete = document.querySelector(".inputDelete")
const newOrderLink = document.querySelector(".newOrderLink")

if(routeCopyBtn !== null){
    routeCopyBtn.addEventListener("click", copyRoute)
}

function copyRoute(){
    this.style.display = "none"
    inputDelete.style.display = "none"
    newOrderLink.style.display = "none"
    inputDispatchForm.action = "/dispatch/order/route/create"
    alert("노선 정보를 불러왔습니다.")
}