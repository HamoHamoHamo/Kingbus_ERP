// MARK: Module화 해줄 Function
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
        getEfficiencyPerMember();

    }
}

const onPopUp = () => {
    document.querySelector(".pop-up-bg-container").style.display = "flex";
}

const closePopUp = () => {
    document.querySelector(".pop-up-bg-container").style.display = "none";
}

const onEstimatePopUp = () => {
    document.querySelector(".estimate-pop-up-bg-container").style.display = "flex";
}

const closeEstimatePopUp = () => {
    document.querySelector(".estimate-pop-up-bg-container").style.display = "none";
}

// MARK: - Today, DayBefore, DayAfter Function
const setToday = () => {
    const today = new Date();
    const todayString = today.toISOString().substring(0, 10);

    // location.replace(`${window.location}?date=${today.toISOString().substring(0, 10)}`)
    document.querySelector(".search-dispatch-path-date").value = todayString;
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

// MARK: Document
// 날짜
const dateField = document.querySelector(".search-dispatch-path-date");
const todayButton = document.querySelector(".dispatch-path-today-button");
const dayBeforeButton = document.querySelector(".day-before-button");
const dayAfterButton = document.querySelector(".day-after-button");

// 검색 필드
const searchButton = document.querySelector(".dispatch-path-search-button"); 
const nameField = document.querySelector(".search-dispatch-path");

// Table
// const detailButtons = document.getElementsByClassName("accident-detail-button");

// 사고처리 견적서
const estimateButton = document.querySelector("#estimate-button");

// 등록
const registerButton = document.querySelector("#register-button");
const completeButton = document.querySelector("#complete-button");
const closeButton = document.querySelector("#close-button");

// 파일
const uploadNameDocument = document.querySelector(".upload-name");
const accidentReportButton = document.querySelector("#accident-report");

// variables
const today = new Date();
const todayString = today.toISOString().substring(0, 10);

let searchObject = {
    name: "", // 노선명
    date: todayString, // 날짜
};

window.onload = () => {
    console.log("========[window onload]========")
    
    // 페이지 접속 시, 오늘 날짜 기준으로 검색 진행
    if (!location.href.includes("?")) {
        updateURL(searchObject);

    } else {
        initializeData();

    }

}

// query에서 가져온 데이터 세팅
const initializeData = () => {
    const queryString = location.href.split("?")[1].split("&");
    for (const data of queryString) {
        let [key, value] = data.split("=");
        if (key === "date" && value === "") {
            value = todayString;

        }

        searchObject[key] = decodeURI(value);

    }

    dateField.value = searchObject.date;
    console.log(searchObject);
    setData();
}

const setData = () => {
    dateField.value = searchObject.date;
    nameField.value = searchObject.name;

}

// eventListener
todayButton.addEventListener("click", () => {
    setToday()
    updateURL(searchObject);
});

dayBeforeButton.addEventListener("click", () => {
    setDayBefore();
    updateURL(searchObject);
});

dayAfterButton.addEventListener("click", () => {
    setDayAfter();
    updateURL(searchObject);
});

dateField.addEventListener("change", () => {
    const date = new Date(dateField.value);
    searchObject.date = date.toISOString().substring(0, 10);
    updateURL(searchObject);
})

searchButton.addEventListener("click", () => {

});

// for (let detailButton of detailButtons) {
//     detailButton.addEventListener("click", () => {
//         console.log("Detail Button Clicked");
//     })
// }

estimateButton.addEventListener("click", () => {
    closePopUp();
    onEstimatePopUp();
})

registerButton.addEventListener("click", () => {
    onPopUp();
});

completeButton.addEventListener("click", () => {
    closePopUp();
})

closeButton.addEventListener("click", () => {
    closePopUp();
})

// accidentReportButton.value.addEventListener("change", () => {
//     console.log("accidentReportButton");
//     let fileName = accidentReportButton.value();
//     console.log(fileName);
//     uploadNameDocument.value = fileName;
// })

// MARK: - Estimate Pop Up