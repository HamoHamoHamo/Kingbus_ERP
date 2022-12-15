const calenderSwitchBtn = document.querySelector(".calendar_switch_btn")
const dispatchOrderSearch = document.querySelector(".dispatch_search_form")

calenderSwitchBtn.addEventListener("click", calenderSwitch)

function calenderSwitch(){
    let parms = new URLSearchParams(location.search)
    let baseUrl = window.location.href.split("?")[0]

    if(parms.has("change")){
        location.href = `${baseUrl}?${window.location.search.split("change=true&")[1]}`
    }else{
        if(parms.has("year")){
            location.href = `${baseUrl}?change=true&year=${parms.get("year")}&month=${parms.get("month")}`
        }else{
            const date = new Date()
            location.href = `${baseUrl}?change=true&year=${date.getFullYear()}&month=${date.getMonth()+1}`
        }
    }
}

function switchBtnName(){
    let parms = new URLSearchParams(location.search)
    
    if(parms.has("change")){
        calenderSwitchBtn.children[1].innerText = "기본달력"
        dispatchOrderSearch.style.display = "flex"
    }else{
        calenderSwitchBtn.children[1].innerText = "배차달력"
        dispatchOrderSearch.style.display = "none"
    }
}

switchBtnName()