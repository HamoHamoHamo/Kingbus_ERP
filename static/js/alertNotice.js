const deletBtn = document.querySelector('.deletBtn')
const tableForm = document.querySelector('.tableForm')

tableForm.addEventListener('submit', blockForm)

function blockForm(e){
    e.preventDefault()
}

deletBtn.addEventListener('click', alertToDelete)

function alertToDelete(){
    console.log(alert('정말로 삭제하시겠습니까?'))
}