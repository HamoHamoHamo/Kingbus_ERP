const clientDeleteBtn = document.querySelector(".clientDeleteBtn")
const clientDeleteForm = document.querySelector(".clientDeleteForm")

clientDeleteBtn.addEventListener("click", deleteClient)

function deleteClient(){
    if(confirm("정말로 삭제하시겠습니까?")){
        clientDeleteForm.submit()
    }
}