// 차량대수랑 배차대수가 다를 떄 파란색으로 표시
function matchDispatch() {
    for (i = 0; i < subContents.length; i++) {
        if (subContents[i].children[1].innerText.split(" (")[0] !== subContents[i].children[1].innerText.split(" (")[1].replace(/\)/g, "")) {
            subContents[i].children[1].style.fontWeight = "700"
            subContents[i].children[1].style.color = "#0069D9"
        }
    }
}