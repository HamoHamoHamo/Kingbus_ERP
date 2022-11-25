const routeCopyBtn = document.querySelector(".routeCopyBtn")
const inputDelete = document.querySelector(".inputDelete")
const newOrderLink = document.querySelector(".newOrderLink")

routeCopyBtn.addEventListener("click", copyRoute)

function copyRoute(){
    this.style.display = "none"
    inputDelete.style.display = "none"
    newOrderLink.style.display = "none"
    inputDispatchForm.action = "/dispatch/order/route/create"
}