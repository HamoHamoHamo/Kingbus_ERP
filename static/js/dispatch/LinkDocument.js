const docmentBtn = document.querySelector(".docmentBtn")

docmentBtn.addEventListener("click", linkDocument)

function linkDocument(){
    location.href = `/document/dispatch?date1=${inputTextquarter[0].value}`
}