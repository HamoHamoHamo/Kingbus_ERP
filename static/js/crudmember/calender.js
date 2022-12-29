const calenderDateBox = document.querySelectorAll(".calenderDateBox")
const todayBtn = document.querySelector(".todayBtn")
const prevBtn = document.querySelector(".prevBtn")
const nextBtn = document.querySelector(".nextBtn")
const dateTitle = document.querySelector(".dateTitle")
const basicContentesArea = document.querySelector(".basicContentesArea")
const orderContentesArea = document.querySelector(".orderContentesArea")
const changeFormatBtn = document.querySelector(".changeFormatBtn")
const search = document.querySelector(".search-Form")


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
            if (AUTHORITY < 3) {
                if (parms.has("change")) {
                    cloneNode = orderContentesArea.cloneNode(true);
                    calenderDateBox[i + 1].children[0].after(cloneNode)
                } else {
                    cloneNode = basicContentesArea.cloneNode(true);
                    calenderDateBox[i + 1].children[0].after(cloneNode)
                }
            }
            if ((parms.get("month") == nowMonth || !parms.has("month"))) {
                if (!calenderDateBox[i].classList.contains("beforeMonth") && !calenderDateBox[i].classList.contains("afterMonth") && thisDateCounter == thisDate) {
                    calenderDateBox[i].children[0].children[0].style.backgroundColor = "#0069D9"
                    calenderDateBox[i].children[0].children[0].style.color = "white"
                }
                thisDateCounter = thisDateCounter + 1
            }
        };
    } else {
        for (i = prevDay; i < 41 - (6 - nowDay); i++) {
            calenderDateBox[i + 1].children[0].children[0].innerText = i - (prevDay - 1)

            if (AUTHORITY < 3) {
                if (parms.has("change")) {
                    cloneNode = orderContentesArea.cloneNode(true);
                    calenderDateBox[i + 1].children[0].after(cloneNode)
                } else {
                    cloneNode = basicContentesArea.cloneNode(true);
                    calenderDateBox[i + 1].children[0].after(cloneNode)
                }
            }
            if ((parms.get("month") == nowMonth || !parms.has("month"))) {
                if (!calenderDateBox[i].classList.contains("beforeMonth") && !calenderDateBox[i].classList.contains("afterMonth") && thisDateCounter == thisDate) {
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
            calenderDateBox[i].classList.add("afterMonth")
        };
    } else {
        for (i = 41; i > 41 - (6 - nowDay); i--) {
            calenderDateBox[i].classList.add("afterMonth")
        };
    }
}




// 날짜선택
for (i = 0; i < calenderDateBox.length; i++) {
    calenderDateBox[i].addEventListener("click", checkThisDate)
};


function checkThisDate() {
    if (!this.classList.contains("beforeMonth") && !this.classList.contains("afterMonth")) {
        for (i = 0; i < calenderDateBox.length; i++) {
            calenderDateBox[i].style.border = "0.2rem solid white"
        };
        this.style.border = "0.2rem solid #0069D9"
        if (parms.has("year") && parms.has("month")) {
            if (parseInt(this.children[0].children[0].innerText) < 10) {
                thisDateData = `${parms.get("year")}-${parms.get("month")}-0${this.children[0].children[0].innerText}`
            } else {
                thisDateData = `${parms.get("year")}-${parms.get("month")}-${this.children[0].children[0].innerText}`
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

// 현재 년, 월
let nowY = parseInt(parms.get("year")) ? parseInt(parms.get("year")) : nowYear;
let nowM = parseInt(parms.get("month")) ? parseInt(parms.get("month")) : nowMonth;



// 이전 버튼
prevBtn.addEventListener("click", prevDay)

function prevDay() {
    let prevM = nowM < 11 ? `0${nowM-1}` : nowM - 1;
    let prevY = nowM == 1 ? nowY - 1 : nowY;
    if (prevM === '00') {
        prevM = 12
    }

    if (parms.has("change")) {
        location.href = `${window.location.href.split("?")[0]}?change=true&year=${prevY}&month=${prevM}`
    } else {
        location.href = `${window.location.href.split("?")[0]}?year=${prevY}&month=${prevM}`
    }
    
}





// 다음 버튼
nextBtn.addEventListener("click", nextDay)

function nextDay() {
    let nextM = nowM < 9 ? `0${nowM+1}` : nowM + 1;
    let nextY = nowM === 12 ? nowY + 1 : nowY;
    if (nextM === 13) {
        nextM = '01'
    }

    if (parms.has("change")) {
        location.href = `${window.location.href.split("?")[0]}?change=true&year=${nextY}&month=${nextM}`
    } else {
        location.href = `${window.location.href.split("?")[0]}?year=${nextY}&month=${nextM}`
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