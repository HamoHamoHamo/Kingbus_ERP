import { Comma } from "/static/js/common/addComma.js"

const updateURL = (search) => {
    let url = `${location.origin}${location.pathname}`
    
    for (const key of Object.keys(search)) {
        if (url.includes("?")) {
            url += `&${key}=${search[key]}`
        } else {
            url += `?${key}=${search[key]}`
        }
    }

    location.href = url;
}

const keyCodeCheck = (event, callBack) => {
    if ((event.key === "Enter" || event.keyCode === 13)) {
        console.log("keyCodeCheck()")
        // getEfficiencyPerMember();

    }
}

// MARK: - Today, DayBefore, DayAfter Function
const setToday = () => {
    const today = new Date();
    const todayString = today.toISOString().substring(0, 10);

    // location.replace(`${window.location}?date=${today.toISOString().substring(0, 10)}`)
    dateField.value = todayString;
    dateField2.value = todayString;
}

const getCalcluatedDate = (days, currentDate=dateField.value) => {
    console.log(currentDate, days)
    // const currentDate = dateField.value;
    let date;
    if (currentDate === "") {
        date = new Date();
    } else {
        date = new Date(currentDate);
    }

    const calcuatedDate = new Date(date.setDate(date.getDate() + days)).toISOString().substring(0, 10);

    return calcuatedDate;
}

const getLastDayOfMonth = (date) => {
    const dateList = date.split('-');
    const lastDayOfMonth = new Date(dateList[0], parseInt(dateList[1]), 0);
    console.log(lastDayOfMonth)
    return lastDayOfMonth.getDate()
}


// MARK: CheckBox
// document
const selectAllCheckBox = document.querySelector(".amountCheckAll");
const selectCheckBox = document.querySelectorAll(".amountCheck");

// variable
let checkCount = 0;

// function
const selectAll = (selectAll) => {
    const checkboxAll = document.querySelectorAll(".amountCheck");

    checkboxAll.forEach((checkbox) => {
        checkbox.checked = selectAll.checked;

        if (selectAll.checked) {
            checkCount = selectCheckBox.length;
            checkbox.classList.add("checked")

        } else {
            checkCount = 0;
            checkbox.classList.remove("checked")

        }
    })
}

// eventListener
selectAllCheckBox.addEventListener("click", () => {
    selectAll(selectAllCheckBox);
});

for (const checkbox of selectCheckBox) {
    const count = selectCheckBox.length;

    checkbox.addEventListener("click", () => {
        checkbox.classList.toggle("checked")

        if (checkbox.classList.contains("checked")) {
            checkCount++;
            if (count === checkCount) {
                selectAllCheckBox.checked = true;

            }

        } else {
            checkCount--;

            selectAllCheckBox.checked = false;
        }

    })
}

// document
// 날짜
const dateField = document.querySelector(".search-dispatch-path-date1");
const dateField2 = document.querySelector(".search-dispatch-path-date2");
const todayButton = document.querySelector(".dispatch-path-today-button");
const dayBeforeButton = document.querySelector(".day-before-button");
const dayAfterButton = document.querySelector(".day-after-button");

// 검색 필드
const searchButton = document.querySelector(".dispatch-path-search-button"); 
const pathNameField = document.querySelector(".search-dispatch-path");
const nameField = document.querySelector(".name-input-td");
const dispatchKindField = document.querySelectorAll(".work-time");
const salaryField = document.querySelector(".salary-input-td");
const contractTypeField = document.querySelector(".salary-form-input-td");
const dailyButton = document.querySelector(".dailyButton");
const weeklyButton = document.querySelector(".weeklyButton");
const monthlyButton = document.querySelector(".monthlyButton");


// Variabels
const today = new Date();
const todayString = today.toISOString().substring(0, 10);
let dispatchKind = "";

for (const eachValue of dispatchKindField) {
    if (eachValue.children[0].checked) {
        dispatchKind = eachValue.children[1].textContent
        break;

    } else {
        dispatchKind = "출근"
        
    }

}

let searchObject = {
    pathName: "", // 노선명
    date1: todayString, // 날짜
    date2: todayString, // 날짜
    name: "", // 이름
    salary: "", // 급여
    dispatchKind: dispatchKind, // 배차 종류(출근, 퇴근, 일반)
    contractType: "" // 급여형태(계약형태)
};

window.onload = () => {
    console.log("========[window onload]========")
    Comma.addCommaToInnerText()
    // 페이지 접속 시, 오늘 날짜 기준으로 검색 진행
    // if (!location.href.includes("?")) {
    //     updateURL(searchObject);

    // } else {
    //     initializeData();

    // }
    initializeData();
    

}

// query에서 가져온 데이터 세팅
const initializeData = () => {
    const queryString = location.href.split("?")[1].split("&");
    for (const data of queryString) {
        let [key, value] = data.split("=");
        if ((key === "date1" && value === "") || 
            (key === "date2" && value === "")) {
            value = todayString;
        }

        searchObject[key] = decodeURI(value);

    }

    dateField.value = searchObject.date1;
    dateField2.value = searchObject.date2;
    console.log(searchObject);
    setData();
}

const setData = () => {
    dateField.value = searchObject.date1;
    dateField2.value = searchObject.date2;
    pathNameField.value = searchObject.pathName;
    nameField.value = searchObject.name;
    salaryField.value = searchObject.salary;
    contractTypeField.value = searchObject.contractType;

    for (const eachValue of dispatchKindField) {
        if (eachValue.children[0].value === searchObject.dispatchKind) {
            eachValue.children[0].checked = true

        }

    }
}

const setDateField = (date1, date2) => {
    dateField.value = date1;
    dateField2.value = date2;
    searchObject.date1 = date1;
    searchObject.date2 = date2;
}

// MARK: - Today, DayBefore, DayAfter Button
// eventListener
todayButton.addEventListener("click", () => {
    setToday();
    updateURL(searchObject);
});

dayBeforeButton.addEventListener("click", () => {
    const calculatedDate = getCalcluatedDate(-1);
    setDateField(calculatedDate, calculatedDate);
    updateURL(searchObject);
});

dayAfterButton.addEventListener("click", () => {
    const calculatedDate = getCalcluatedDate(1);
    setDateField(calculatedDate, calculatedDate);
    updateURL(searchObject);
});

dailyButton.addEventListener("click", () => {
    searchObject.dateType="daily";
    setDateField(dateField.value, dateField.value);
    updateURL(searchObject);
})

weeklyButton.addEventListener("click", () => {
    searchObject.dateType="weekly";
    const calculatedDate = getCalcluatedDate(7);
    setDateField(dateField.value, calculatedDate);
    updateURL(searchObject);
})

monthlyButton.addEventListener("click", () => {
    searchObject.dateType="monthly";
    const firstDate = dateField.value.substring(0, 8) + "01";
    const calculatedDate = getCalcluatedDate(getLastDayOfMonth(dateField.value) - 1, firstDate);

    setDateField(firstDate, calculatedDate);
    updateURL(searchObject);
})

// MARK: API 통신
// const getEfficiencyPerMember = () => {
//     console.log("getEfficiencyPerMember");
//     response = $.ajax({
//         url: "",
//         method: "GET",
//         data: searchObject,
//         datatype: 'json',
//         success: () => {
//             console.log("success")
//         },
//         error: (request, error) => {
//             console.log(`CODE: ${request.status}` + "\n" + `message: ${error}`)
//         }
//     })
// }

// eventListener

document.addEventListener("keypress", event => keyCodeCheck(event));
