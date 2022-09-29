const docmentBtn = document.querySelector(".docmentBtn")

docmentBtn.addEventListener("click", linkDocument)

function linkDocument() {
    if (window.location.search.split("&")[0].substr(0, 3) == "?id") {
        location.href = `/document/dispatch?date1=${inputTextquarter[0].value}&date2=${inputTextquarter[1].value}`
    }
}