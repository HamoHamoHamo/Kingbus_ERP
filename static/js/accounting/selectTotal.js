const depositCell = document.querySelectorAll(".depositCell")
const selectTotal = document.querySelector(".selectTotalPrice")

for (i = 0; i < depositCell.length; i++) {
    depositCell[i].addEventListener("click", totalSelecting)
};

function totalSelecting() {
    if (!this.classList.contains("selecting")) {
        this.classList.add("selecting")
        selectTotal.innerText = parseInt(selectTotal.innerText.replace(/\,/g, "")) + parseInt(this.children[5].innerText.replace(/\,/g, "")) + parseInt(this.children[6].innerText.replace(/\,/g, ""))
        selectTotal.innerText = selectTotal.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    } else {
        this.classList.remove("selecting")
        selectTotal.innerText = parseInt(selectTotal.innerText.replace(/\,/g, "")) - (parseInt(this.children[5].innerText.replace(/\,/g, "")) + parseInt(this.children[6].innerText.replace(/\,/g, "")))
        selectTotal.innerText = selectTotal.innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    }
}
