const calenderDateBox = document.querySelectorAll(".calenderDateBox")
const todayBtn = document.querySelector(".todayBtn")
const prevBtn = document.querySelector(".prevBtn")
const nextBtn = document.querySelector(".nextBtn")
const dateTitle = document.querySelector(".dateTitle")
const basicContentesArea = document.querySelector(".basicContentesArea")
const orderContentesArea = document.querySelector(".orderContentesArea")
const changeFormatBtn = document.querySelector(".changeFormatBtn")
const search = document.querySelector(".controllArea form")


let parms = new URLSearchParams(location.search)

const date = new Date()

const nowYear = new Date(date).getFullYear();
const nowMonth = new Date(date).getMonth() + 1;

let thisDate = date.getDate();

let thisDateData = "";

calender()

function calender() {

    let prevDay = ""
    let nowDay = ""

    if (parms.has("year") && parms.has("month")) {
        prevDay = new Date(parms.get("year"), parms.get("month") - 1, 0).getDay();
        nowDay = new Date(parms.get("year"), parms.get("month"), 0).getDay();

        dateTitle.innerText = `${parms.get("year")}년 ${parms.get("month")}월`
    } else {
        prevDay = new Date(nowYear, nowMonth - 1, 0).getDay();
        nowDay = new Date(nowYear, nowMonth, 0).getDay();

        dateTitle.innerText = `${nowYear}년 ${nowMonth}월`
    }

    if (parms.has("change")) {
        search.style.display = "flex"
        changeFormatBtn.children[1].innerText = "기본달력"
    }

    prevMonth(prevDay)
    thisMonth(prevDay, nowDay)
    nextMonth(nowDay)
}

function prevMonth(prevDay) {
    for (i = 0; i <= prevDay; i++) {
        calenderDateBox[i].classList.add("beforeMonth")
    };
}


function thisMonth(prevDay, nowDay) {
    let cloneNode = ""
    let thisDateCounter = 0
    if (41 - (6 - nowDay) >= 38) {
        for (i = prevDay; i < 41 - (6 - nowDay) - 7; i++) {
            calenderDateBox[i + 1].children[0].children[0].innerText = i - (prevDay - 1)
            if (parms.has("change")) {
                cloneNode = orderContentesArea.cloneNode(true);
                calenderDateBox[i + 1].children[0].after(cloneNode)
            } else {
                cloneNode = basicContentesArea.cloneNode(true);
                calenderDateBox[i + 1].children[0].after(cloneNode)
            }
            if ((parms.get("month") == nowMonth || !parms.has("month"))) {
                if (!calenderDateBox[i].classList.contains("beforeMonth") && thisDateCounter == thisDate) {
                    calenderDateBox[i].children[0].children[0].style.backgroundColor = "#0069D9"
                    calenderDateBox[i].children[0].children[0].style.color = "white"
                }
                thisDateCounter = thisDateCounter + 1
            }
        };
    } else {
        for (i = prevDay; i < 41 - (6 - nowDay); i++) {
            calenderDateBox[i + 1].children[0].children[0].innerText = i - (prevDay - 1)
            if (parms.has("change")) {
                cloneNode = orderContentesArea.cloneNode(true);
                calenderDateBox[i + 1].children[0].after(cloneNode)
            } else {
                cloneNode = basicContentesArea.cloneNode(true);
                calenderDateBox[i + 1].children[0].after(cloneNode)
            }
            if ((parms.get("month") == nowMonth || !parms.has("month"))) {
                if (!calenderDateBox[i].classList.contains("beforeMonth") && thisDateCounter == thisDate) {
                    calenderDateBox[i].children[0].children[0].style.backgroundColor = "#0069D9"
                    calenderDateBox[i].children[0].children[0].style.color = "white"
                }
                thisDateCounter = thisDateCounter + 1
            }
        };
    }
}

function nextMonth(nowDay) {
    if (41 - (6 - nowDay) >= 38) {
        for (i = 41; i > 41 - (6 - nowDay) - 7; i--) {
            calenderDateBox[i].classList.add("beforeMonth")
        };
    } else {
        for (i = 41; i > 41 - (6 - nowDay); i--) {
            calenderDateBox[i].classList.add("beforeMonth")
        };
    }
}




// 날짜선택
for (i = 0; i < calenderDateBox.length; i++) {
    calenderDateBox[i].addEventListener("click", checkThisDate)
};


function checkThisDate() {
    if (!this.classList.contains("beforeMonth")) {
        for (i = 0; i < calenderDateBox.length; i++) {
            calenderDateBox[i].style.border = "0.2rem solid white"
        };
        this.style.border = "0.2rem solid #0069D9"
        if (parms.has("year") && parms.has("month")) {
            if (parseInt(this.children[0].children[0].innerText) < 10) {
                thisDateData = `${parms.get("year")}-${parms.get("menth")}-0${this.children[0].children[0].innerText}`
            } else {
                thisDateData = `${parms.get("year")}-${parms.get("menth")}-${this.children[0].children[0].innerText}`
            }
        } else {
            if (parseInt(this.children[0].children[0].innerText) < 10) {
                thisDateData = `${nowYear}-${nowMonth}-0${this.children[0].children[0].innerText}`
            } else {
                thisDateData = `${nowYear}-${nowMonth}-${this.children[0].children[0].innerText}`
            }
        }
    }
}






// 오늘 버튼
todayBtn.addEventListener("click", today)

function today() {
    if (parms.has("change")) {
        location.href = `${window.location.href.split("?")[0]}?change=true`
    } else {
        location.href = `${window.location.href.split("?")[0]}`
    }
}





// 이전 버튼
prevBtn.addEventListener("click", prevDay)

function prevDay() {
    if (parms.has("year") && parms.has("month")) {
        if (parms.get("month") == 1) {
            if (parms.has("change")) {
                location.href = `${window.location.href.split("?")[0]}?change=true&year=${parseInt(parms.get("year")) - 1}&month=${12}`
            } else {
                location.href = `${window.location.href.split("?")[0]}?year=${parseInt(parms.get("year")) - 1}&month=${12}`
            }
        } else {
            if (parms.has("change")) {
                location.href = `${window.location.href.split("?")[0]}?change=true&year=${parms.get("year")}&month=${parseInt(parms.get("month")) - 1}`
            } else {
                location.href = `${window.location.href.split("?")[0]}?year=${parms.get("year")}&month=${parseInt(parms.get("month")) - 1}`
            }
        }
    } else {
        if (parms.has("change")) {
            location.href = `${window.location.href}&year=${nowYear}&month=${nowMonth - 1}`
        }else{
            location.href = `${window.location.href}?year=${nowYear}&month=${nowMonth - 1}`
        }
    }
}





// 다음 버튼
nextBtn.addEventListener("click", nextDay)

function nextDay() {
    if (parms.has("year") && parms.has("month")) {
        if (parms.get("month") == 12) {
            if (parms.has("change")) {
                location.href = `${window.location.href.split("?")[0]}?change=true&year=${parseInt(parms.get("year")) + 1}&month=${1}`
            } else {
                location.href = `${window.location.href.split("?")[0]}?year=${parseInt(parms.get("year")) + 1}&month=${1}`
            }
        } else {
            if (parms.has("change")) {
                location.href = `${window.location.href.split("?")[0]}?change=true&year=${parms.get("year")}&month=${parseInt(parms.get("month")) + 1}`
            } else {
                location.href = `${window.location.href.split("?")[0]}?year=${parms.get("year")}&month=${parseInt(parms.get("month")) + 1}`
            }
        }
    } else {
        if (parms.has("change")) {
            location.href = `${window.location.href}?change=true&year=${nowYear}&month=${nowMonth + 1}`
        } else {
            location.href = `${window.location.href}?year=${nowYear}&month=${nowMonth + 1}`
        }
    }
}




// 달력 폼 바꾸기
changeFormatBtn.addEventListener("click", changeForm)

function changeForm() {
    location.href = `${window.location.href}?year=${nowYear}&month=${nowMonth + 1}`
    if (parms.has("year") && parms.has("month")) {
        if (parms.has("change")) {
            location.href = `${window.location.href.split("?")[0]}?year=${parms.get("year")}&month=${parms.get("month")}`
        } else {
            location.href = `${window.location.href.split("?")[0]}?change=true&year=${parms.get("year")}&month=${parms.get("month")}`
        }
    } else if (parms.has("change")) {
        location.href = `${window.location.href.split("?")[0]}`
    } else {
        location.href = `${window.location.href}?change=true`
    }
}