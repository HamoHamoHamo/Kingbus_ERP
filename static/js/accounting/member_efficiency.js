import { addCommaToInnerText } from "../common/addComma.js"

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

const setCalcluatedDay = (days) => {
    const currentDate = dateField.value;
    let date;
    if (currentDate === "") {
        date = new Date();
    } else {
        date = new Date(currentDate);
    }

    const calcuatedDate = new Date(date.setDate(date.getDate() + days)).toISOString().substring(0, 10);

    dateField.value = calcuatedDate;
    dateField2.value = calcuatedDate;
    searchObject.date1 = calcuatedDate;
    searchObject.date2 = calcuatedDate;
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
    
    // 페이지 접속 시, 오늘 날짜 기준으로 검색 진행
    if (!location.href.includes("?")) {
        updateURL(searchObject);

    } else {
        initializeData();

    }
    addCommaToInnerText()

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

// MARK: - Today, DayBefore, DayAfter Button
// eventListener
todayButton.addEventListener("click", () => {
    setToday()
    updateURL(searchObject);
});

dayBeforeButton.addEventListener("click", () => {
    setCalcluatedDay(-1);
    updateURL(searchObject);
});

dayAfterButton.addEventListener("click", () => {
    setCalcluatedDay(+1);
    updateURL(searchObject);
});


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
