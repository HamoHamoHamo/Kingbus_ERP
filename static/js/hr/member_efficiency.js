// MARK: - 차트 세팅
// const totalChart = document.querySelector(".total-run-pie-chart");
// const totalChartMainValue = document.querySelector(".total-run-pie-chart-center")

// const personalChart = document.querySelector(".personal-run-pie-chart")
// const personalChartMainValue = document.querySelector(".personal-run-pie-chart-center")

// const setTotalChart = (percent) => {
//     totalChart.style.background = `conic-gradient(#3D36FF 25% ${percent}%, #FF8585 0% ${100 - percent}%)`
//     totalChartMainValue.textContent = `${percent}%`

// }

// const setPersonalChart = (percent) => {
//     personalChart.style.background = `conic-gradient(#3D36FF 25% ${percent}%, #EFFF8D 0% ${100 - percent}%)`
//     personalChartMainValue.textContent = `${percent}%`

// }

// setTotalChart(54);
// setPersonalChart(86);

// Object Variabels
let searchObject;

// localStorage function
const setSearchObject = (searchKey, searchValue) => {
    if (searchKey) {
        searchObject[searchKey] = searchValue
    }
    localStorage.setItem("member/efficiency/search", JSON.stringify(searchObject))
}

const getSearchObject = (searchKey) => {
    const searchItem = JSON.parse(localStorage.getItem("member/efficiency/search"));
    const result = searchKey == undefined ? searchItem : searchItem[searchKey];

    return result
}

const updateURL = () => {
    let url = `${location.origin}${location.pathname}`
    const search = getSearchObject();
    
    for (const key of Object.keys(search)) {
        console.log(key);
        if (search[key] !== "") {
            if (url.includes("?")) {
                url += `&${key}=${search[key]}`
            } else {
                url += `?${key}=${search[key]}`
            }
        }
    }

    location.href = url;
}

// Models
if (localStorage.getItem("member/efficiency/search")) {
    searchObject = getSearchObject();
    setSearchObject();

} else {
    localStorage.clear();
    const today = new Date();
    const todayString = today.toISOString().substring(0, 10);

    searchObject = {
        pathName: "", // 노선명
        date: todayString, // 날짜
        name: "", // 이름
        salary: "", // 급여
        dispatchKind: "", // 배차 종류(출근, 퇴근, 일반)
        contractType: "" // 급여형태(계약형태)
    };
    setSearchObject();

}

const tableObject = {

}

// MARK: - Today, DayBefore, DayAfter Button
// document
const dateField = document.querySelector(".search-dispatch-path-date");
const todayButton = document.querySelector(".dispatch-path-today-button");
const dayBeforeButton = document.querySelector(".day-before-button");
const dayAfterButton = document.querySelector(".day-after-button");

// variable

// function
const changeDateFieldValue = () => {
    setSearchObject("date", dateField.value);
}

const setToday = () => {
    const today = new Date();
    const todayString = today.toISOString().substring(0,10);

    // location.replace(`${window.location}?date=${today.toISOString().substring(0, 10)}`)
    document.querySelector(".search-dispatch-path-date").value = todayString;
    setSearchObject("date", todayString);
}

const setDayBefore = () => {
    const currentDate = document.querySelector(".search-dispatch-path-date").value;
    let date;
    if (currentDate === "") {
        date = new Date();
    } else {
        date = new Date(currentDate);
    }

    const yesterday = new Date(date.setDate(date.getDate() - 1));

    document.querySelector(".search-dispatch-path-date").value = yesterday.toISOString().substring(0, 10);
    setSearchObject("date", yesterday.toISOString().substring(0,10));
}

const setDayAfter = () => {
    const currentDate = document.querySelector(".search-dispatch-path-date").value;
    let date;
    if (currentDate === "") {
        date = new Date();
    } else {
        date = new Date(currentDate);
    }
    
    const tomorrow = new Date(date.setDate(date.getDate() + 1));

    document.querySelector(".search-dispatch-path-date").value = tomorrow.toISOString().substring(0, 10);
    setSearchObject("date", tomorrow.toISOString().substring(0, 10));
}

// eventListener
todayButton.addEventListener("click", () => {
    setToday()
    updateURL();
});

dayBeforeButton.addEventListener("click", () => {
    setDayBefore();
    updateURL();
});

dayAfterButton.addEventListener("click", () => {
    setDayAfter();
    updateURL();
});

dateField.addEventListener("change", () => {
    changeDateFieldValue();
    updateURL();
})

// MARK: Search
// document
const searchButton = document.querySelector(".dispatch-path-search-button");
const pathNameField = document.querySelector(".search-dispatch-path");
const nameField = document.querySelector(".name-input-td");
const workTimeField = document.querySelectorAll(".work-time");
const salaryField = document.querySelector(".salary-input-td");
const contractTypeField = document.querySelector(".salary-form-input-td");

// variable

// function
const search = () => {
    let [pathName, name, salary, contractType] = [pathNameField.value, nameField.value, salaryField.value, contractTypeField.value];

    setSearchObject("pathName", pathName);
    setSearchObject("name", name);
    setSearchObject("salary", salary);
    setSearchObject("contractType", contractType);
    for (const eachValue of workTimeField) {
        if (eachValue.children[0].checked) {
            setSearchObject("dispatchKind", eachValue.children[1].textContent);
            break;

        }
        
    }
}

// eventListener
searchButton.addEventListener("click", () => {
    search();
    updateURL();
});

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

// MARK: 세팅
const setting = () => {
    dateField.value = getSearchObject("date");
    pathNameField.value = getSearchObject("pathName");
    nameField.value = getSearchObject("name");
    workTimeField.value = getSearchObject("dispatchKind");
    salaryField.value = getSearchObject("salary");
    contractTypeField.value = getSearchObject("contractType");
    
}

setting();