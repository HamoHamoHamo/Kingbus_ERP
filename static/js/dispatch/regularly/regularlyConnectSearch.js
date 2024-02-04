const groupListItem = document.querySelectorAll(".groupOpen")
const teamCheckAll = document.querySelector("#teamCheckAll")
const teamCheckboxList = document.querySelectorAll(".teamCheckbox")
const timeCheckAll = document.querySelector("#timeCheckAll")
const timeCheckboxList = document.querySelectorAll(".timeCheckbox")

// 사업장 열기
for (i = 0; i < groupListItem.length; i++) {
    groupListItem[i].addEventListener("click", openGroup)
}

function openGroup() {
    const innerDetailItem = this.parentNode.nextElementSibling
    const checkboxList = innerDetailItem.querySelectorAll("input")
    // console.log("TEST", innerDetailItem.querySelectorAll("input"))

    if (this.parentNode.children[1].classList.contains("openGroup")) {
        this.parentNode.children[1].classList.remove("openGroup")
        innerDetailItem.style.display = "none"
        checkboxChecked(checkboxList, false)
    } else {
        this.parentNode.children[1].classList.add("openGroup")
        innerDetailItem.style.display = "flex"
        checkboxChecked(checkboxList, true)
    }
}

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
            console.log("checkbox.parentNode.parentNode.parentNode", businessCheckboxList[i].parentNode.parentNode.parentNode)
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
    for (let i = 0; i < searchTeamList.length; i++) {
        if (checkbox.value == searchTeamList[i]) {
            checkbox.checked = true
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
    // 팀목록 검색한 값 체크하기
    for (let i = 0; i < searchTimeList.length; i++) {
        if (checkbox.value == searchTimeList[i]) {
            checkbox.checked = true
        }
    }
})

function timeCheckAllCheckFalse() {
    timeCheckAll.checked = false
}
