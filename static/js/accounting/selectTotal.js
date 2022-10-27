const depositCell = document.querySelectorAll(".depositCell")
const selectTotal = document.querySelector(".selectTotalPrice")

for (i = 0; i < depositCell.length; i++) {
    depositCell[i].children[6].addEventListener("click", totalSelecting)
    depositCell[i].children[7].addEventListener("click", totalSelecting)
};

function totalSelecting() {
    if (!this.parentNode.classList.contains("selecting")) {
        this.parentNode.classList.add("selecting")
        selectTotal.innerText = parseInt(selectTotal.innerText.replace(/\,/g, "")) + parseInt(this.parentNode.children[6].innerText.replace(/\,/g, "")) + parseInt(this.parentNode.children[7].innerText.replace(/\,/g, ""))
        selectTotal.innerText = selectTotal.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    } else {
        this.parentNode.classList.remove("selecting")
        selectTotal.innerText = parseInt(selectTotal.innerText.replace(/\,/g, "")) - (parseInt(this.parentNode.children[6].innerText.replace(/\,/g, "")) + parseInt(this.parentNode.children[7].innerText.replace(/\,/g, "")))
        selectTotal.innerText = selectTotal.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    }
}
