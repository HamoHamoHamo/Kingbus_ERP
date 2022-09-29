const documentDate = document.querySelectorAll(".searchDataBox input")

window.onload = function () {
    let params = new URLSearchParams(document.location.search)
    if(window.location.search !== ""){
        documentDate[0].value = params.get("date1")
        documentDate[1].value = params.get("date2")
    }
}