const teamCheckAll = document.querySelector("#teamCheckAll")
const teamCheckboxList = document.querySelectorAll(".teamCheckbox")
const timeCheckAll = document.querySelector("#timeCheckAll")
const timeCheckboxList = document.querySelectorAll(".timeCheckbox")
const searchForm = document.querySelector(".searchForm")



searchForm.addEventListener('submit', e => {
    e.preventDefault()
    

    const teamCheck = Array.from(teamCheckboxList).filter(checkbox => checkbox.checked == true)
    console.log(teamCheck)
    if (teamCheck.length == 0) {
        window.alert("팀을 선택해 주세요.")
        return
    }
    const timeCheck = Array.from(timeCheckboxList).filter(checkbox => checkbox.checked == true)
    console.log(timeCheck)
    if (timeCheck.length == 0) {
        window.alert("시간을 선택해 주세요.")
        return
    }
    searchForm.submit()
})


function checkboxChecked(checkboxList, value) {
    Array.from(checkboxList).map((checkbox) => {
        checkbox.checked = value
    })
}


// 검색한 값 체크하기
const businessCheckboxList = document.querySelectorAll(".detailItemBox input")

for (let i = 0; i < businessCheckboxList.length; i++) {
    for (let j = 0; j < searchGroupList.length; j++) {
        if (businessCheckboxList[i].value == searchGroupList[j]) {
            businessCheckboxList[i].checked = true
            // console.log("checkbox.parentNode.parentNode.parentNode", businessCheckboxList[i].parentNode.parentNode.parentNode)
            businessCheckboxList[i].parentNode.parentNode.parentNode.style.display = "flex"
        }
    }
}




// 팀목록 전체 체크 
teamCheckAll.addEventListener("click", teamCheckboxCheckAll)
function teamCheckboxCheckAll() {
    checkboxChecked(teamCheckboxList, teamCheckAll.checked)
}

Array.from(teamCheckboxList).map((checkbox) => {
    checkbox.addEventListener("click", teamCheckAllCheckFalse)
    // 팀목록 검색한 값 체크하기
    if (searchTeamList) {
        for (let i = 0; i < searchTeamList.length; i++) {
            if (checkbox.value == searchTeamList[i]) {
                checkbox.checked = true
            }
        }
    }
})

function teamCheckAllCheckFalse() {
    teamCheckAll.checked = false
}

// 시간 전체 체크 

timeCheckAll.addEventListener("click", timeCheckboxCheckAll)
function timeCheckboxCheckAll() {
    checkboxChecked(timeCheckboxList, timeCheckAll.checked)
}

Array.from(timeCheckboxList).map((checkbox) => {
    checkbox.addEventListener("click", timeCheckAllCheckFalse)
    // 시간목록 검색한 값 체크하기
    if (searchTimeList) {
        for (let i = 0; i < searchTimeList.length; i++) {
            if (checkbox.value == searchTimeList[i]) {
                checkbox.checked = true
            }
        }
    }
})

function timeCheckAllCheckFalse() {
    timeCheckAll.checked = false
}
