const groupOpen = document.querySelectorAll(".documentContentsTable thead tr td:nth-child(2)")
const group = document.querySelectorAll(".documentContentsTable thead tr")
const fileArea = document.querySelectorAll(".documentContentsTable tbody")

for (i = 0; i < groupOpen.length; i++) {
    groupOpen[i].addEventListener("click", openFileArea)
}

function openFileArea() {
    if (!this.parentNode.parentNode.parentNode.children[1].classList.contains("openFolder")) {
        this.parentNode.parentNode.parentNode.children[1].classList.add("openFolder")
    }else{
        this.parentNode.parentNode.parentNode.children[1].classList.remove("openFolder")
    }
}
