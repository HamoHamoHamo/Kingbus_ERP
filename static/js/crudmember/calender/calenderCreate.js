const calnederDateBox = document.querySelectorAll(".calender_date_box")
const scheduleNormalClone = document.querySelector(".calender_contants_box")
const scheduleOrderClone = document.querySelector(".calender_order_box")

function createCalender() {
    let parms = new URLSearchParams(location.search)
    const date = new Date()
    let prevDay = ""
    let lastDay = ""
    let nextDay = ""
    let toDay = ""

    toDay = date.getDate()

    if (parms.has("year")) {
        prevDay = new Date(parms.get("year"), parms.get("month") - 1, 0).getDay();
        if (parms.get("month") === "12") {
            lastDay = new Date(parseInt(parms.get("year")) + 1, 0, 0).getDate();
        } else {
            lastDay = new Date(parms.get("year"), parms.get("month"), 0).getDate();
        }
        nextDay = new Date(parms.get("year"), parms.get("month"), 0).getDay();
    } else {
        prevDay = new Date(date.getFullYear(), date.getMonth(), 0).getDay();
        if (date.getMonth() === 11) {
            lastDay = new Date(parseInt(date.getFullYear()) + 1, 0, 0).getDate();
        } else {
            lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
        }
        nextDay = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDay();
    }

    for (i = 0; i < prevDay + 1; i++) {
        calnederDateBox[i].classList.add("not_this_month")
    };

    for (i = prevDay + 1; i < prevDay + lastDay + 1; i++) {
        calnederDateBox[i].children[0].children[0].innerText = i - prevDay

        if (!parms.has("year") || parms.get("year") == date.getFullYear() && parms.get("month") == date.getMonth() + 1) {
            if (i === prevDay + toDay) {
                calnederDateBox[i].children[0].children[0].classList.add("today")
            }
        }

        if (AUTHORITY < 3) {
            if (!parms.has("change")) {
                cloneNode = scheduleNormalClone.cloneNode(true);
                calnederDateBox[i].children[0].after(cloneNode)
            } else {
                cloneNode = scheduleOrderClone.cloneNode(true);
                calnederDateBox[i].children[0].after(cloneNode)
            }
        }
    };

    for (i = prevDay + lastDay + 1; i < 42; i++) {
        calnederDateBox[i].classList.add("not_this_month")
    };
}

createCalender()