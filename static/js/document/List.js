const listCheck = document.querySelectorAll(".documentTbody tr")

for (i = 0; i < listCheck.length; i++) {
    listCheck[i].addEventListener("click", checkingRadio)
}

function checkingRadio() {
    this.children[0].children[0].checked = true
}