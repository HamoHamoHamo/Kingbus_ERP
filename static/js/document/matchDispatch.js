const match = document.querySelectorAll(".documentTbody td:nth-child(6)")

window.onload = function matchDispatch() {
    for (i = 0; i < match.length; i++) {
        if (match[i].innerText.split(" (")[0] !== match[i].innerText.split(" (")[1].split(")대")[0]) {
            match[i].style.fontWeight = "700"
            match[i].style.color = "#0069D9"
        }
    }
}