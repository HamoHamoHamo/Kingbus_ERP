const groupListItem = document.querySelectorAll(".groupOpen")
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

// 노선 전체 체크
const connectCheckAll = document.querySelector('.connectCheckAll')
const connectCheckList = document.querySelectorAll('.connectCheck')
connectCheckAll.addEventListener("click", () => {
    checkboxChecked(connectCheckList, connectCheckAll.checked)
})

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

const routeInputScan = document.querySelector(".routeInputScan")

routeInputScan.addEventListener('click', () => {
    const checkboxes = document.querySelectorAll('.connectCheck:checked');
    const date = document.querySelector('.searchDate').value
    
    // 선택된 값들만 배열로 추출
    const selectedValues = Array.from(checkboxes).map(checkbox => checkbox.value);


    // 선택된 값이 없으면 알림
    if (selectedValues.length === 0) {
        alert("최소 하나의 노선을 선택해 주세요.");
        return;
    }

    // 쿼리 문자열 생성
    const queryString = `?date=${date}&values=${selectedValues.join(',')}`;

    // URL 생성 (예: "/your-endpoint")
    const url = `${DISPATCH_PRINT_URL}${queryString}`;
    
    // 새 창 열기
    const popupOptions = "width=1640, height=640,scrollbars=yes";
    window.open(url, '_blank', popupOptions);

})