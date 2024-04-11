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

// MARK: - Today, DayBefore, DayAfter Button
// document
const todayButton = document.querySelector(".dispatch-path-today-button");
const dayBeforeButton = document.querySelector(".day-before-button");
const dayAfterButton = document.querySelector(".day-after-button");

// function
const setToday = () => {
    const today = new Date();

    document.querySelector(".search-dispatch-path-date").value = today.toISOString().substring(0,10);
}

const setDayBefore = () => {
    const currentDate = document.querySelector(".search-dispatch-path-date").value;
    let date;
    if (currentDate === "") {
        date = new Date();
    } else {
        date = new Date(currentDate);
    }

    const tomorrow = new Date(date.setDate(date.getDate() - 1));

    document.querySelector(".search-dispatch-path-date").value = tomorrow.toISOString().substring(0, 10);
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

// eventListener
todayButton.addEventListener("click", () => {
    setToday();
});

dayBeforeButton.addEventListener("click", () => {
    setDayBefore();
});

dayAfterButton.addEventListener("click", () => {
    setDayAfter();
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