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