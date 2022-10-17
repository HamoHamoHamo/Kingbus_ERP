const validation = document.querySelectorAll(".RouteListBodyTr")

// 콤마 추가
function addComma() {
    for (i = 0; i < validation.length; i++) {
        validation[i].children[7].innerText = validation[i].children[7].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        validation[i].children[8].innerText = validation[i].children[8].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    }
}