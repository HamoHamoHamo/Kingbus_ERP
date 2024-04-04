// MARK: - 차트 세팅
const totalChart = document.querySelector(".total-run-pie-chart");
const totalChartMainValue = document.querySelector(".total-run-pie-chart-center")

const personalChart = document.querySelector(".personal-run-pie-chart")
const personalChartMainValue = document.querySelector(".personal-run-pie-chart-center")

const setTotalChart = (percent, notDispatchCount) => {
    const success = percent * 3.6;
    const notDispatch = notDispatchCount * 3.6;
    const failure = 360 - (success + notDispatch);
    console.log(success, notDispatch, failure);

    totalChart.style.background = `conic-gradient(#3D36FF ${success}deg, #FF8585 ${success}deg ${success + failure}deg, #EFFF8D ${success + failure}deg)`;
    totalChartMainValue.textContent = `${percent}%`;

}

const setPersonalChart = (percent) => {
    personalChart.style.background = `conic-gradient(#3D36FF 0% ${percent}%, #EFFF8D 0% ${100 - percent}%)`;
    personalChartMainValue.textContent = `${percent}%`;

}

setTotalChart(54, 20);
setPersonalChart(86);

// MARK: - Today, DayBefore, DayAfter Button
const setToday = () => {
    const today = new Date();

    document.querySelector(".search-dispatch-path-date").value = today.toISOString().substring(0, 10);
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