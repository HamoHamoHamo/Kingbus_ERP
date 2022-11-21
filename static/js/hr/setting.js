function setting() {
    let parms = new URLSearchParams(document.location.search)
    var date = new Date();
    dateYear = date.getFullYear();
    dateMonth = date.getMonth() + 1;

    if (!parms.has("date")) {
        month.value = `${dateYear}-${dateMonth}`
    }
}

setting()