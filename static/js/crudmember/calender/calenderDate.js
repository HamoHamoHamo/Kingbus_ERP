const prevBtn = document.querySelector(".prev_btn")
const nextBtn = document.querySelector(".next_btn")
const calenderDate = document.querySelector(".calender_date")


// 오늘 날짜 표시
function dateControll(){
    const date = new Date()
    let parms = new URLSearchParams(location.search)

    if(!parms.has("year")){
        calenderDate.innerText = `${date.getFullYear()}년 ${date.getMonth() + 1}월`
    }else{
        calenderDate.innerText = `${parms.get("year")}년 ${parms.get("month")}월`
    }
}

dateControll()



// 이전 버튼
prevBtn.addEventListener("click", prevBtnFtn)

function prevBtnFtn(){
    const date = new Date()
    let parms = new URLSearchParams(location.search)
    let baseUrl = window.location.href.split("?")[0]

    if(parms.has("year")){
        if(parms.has("change")){
            location.href = `${baseUrl}?change=true&year=${parms.get("month") === "1" ? parms.get("year") - 1 : parms.get("year")}&month=${parms.get("month") === "1" ? 12 : parms.get("month") - 1}`
        }else{
            location.href = `${baseUrl}?year=${parms.get("month") === "1" ? parms.get("year") - 1 : parms.get("year")}&month=${parms.get("month") === "1" ? 12 : parms.get("month") - 1}`
        }
    }else{
        if(parms.has("change")){
            location.href = `${baseUrl}?change=true&year=${date.getMonth() === 0 ? date.getFullYear() - 1 : date.getFullYear()}&month=${date.getMonth() === 0 ? 12 : date.getMonth()}`
        }else{
            location.href = `${baseUrl}?year=${date.getMonth() === 0 ? date.getFullYear() - 1 : date.getFullYear()}&month=${date.getMonth() === 0 ? 12 : date.getMonth()}`
        }
    }
}



// 다음 버튼
nextBtn.addEventListener("click", nextBtnFtn)

function nextBtnFtn(){
    const date = new Date()
    let parms = new URLSearchParams(location.search)
    let baseUrl = window.location.href.split("?")[0]

    if(parms.has("year")){
        if(parms.has("change")){
            location.href = `${baseUrl}?change=true&year=${parms.get("month") === "12" ? parseInt(parms.get("year")) + 1 : parms.get("year")}&month=${parms.get("month") === "12" ? 1 : parseInt(parms.get("month")) + 1}`
        }else{
            location.href = `${baseUrl}?year=${parms.get("month") === "12" ? parseInt(parms.get("year")) + 1 : parms.get("year")}&month=${parms.get("month") === "12" ? 1 : parseInt(parms.get("month")) + 1}`
        }
    }else{
        if(parms.has("change")){
            location.href = `${baseUrl}?change=true&year=${date.getMonth() === 11 ? parseInt(date.getFullYear()) + 1 : date.getFullYear()}&month=${date.getMonth() === 11 ? 1 : date.getMonth() + 1}`
        }else{
            location.href = `${baseUrl}?year=${date.getMonth() === 11 ? parseInt(date.getFullYear()) + 1 : date.getFullYear()}&month=${date.getMonth() === 11 ? 1 : date.getMonth() + 1}`
        }
    }
}