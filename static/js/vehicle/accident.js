// Object Variabels
let searchObject;
let accidentObject;

// localStorage function
// const setAccidentObject = (accidentKey, accidentValue) => {
//     if (accidentKey) {
//         accidentObject[accidentKey] = accidentValue
//     }
//     localStorage.setItem("vehicle/accident", JSON.stringify(accidentObject))
// }

// const getAccidentObject = (accidentKey) => {
//     const accidentItem = JSON.parse(localStorage.getItem("vehicle/accident"));
//     const result = accidentKey == undefined ? accidentItem : accidentItem[accidentKey];

//     return result
// }

// localStorage function
const setSearchObject = (searchKey, searchValue) => {
    if (searchKey) {
        searchObject[searchKey] = searchValue
    }
    localStorage.setItem("vehicle/accident/search", JSON.stringify(searchObject))
}

const getSearchObject = (searchKey) => {
    const searchItem = JSON.parse(localStorage.getItem("vehicle/accident/search"));
    const result = searchKey == undefined ? searchItem : searchItem[searchKey];

    return result
}

const updateURL = () => {
    let url = `${location.origin}${location.pathname}`
    const search = getSearchObject();

    for (const key of Object.keys(search)) {
        
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
if (localStorage.getItem("vehicle/accident/search")) {
    searchObject = getSearchObject();
    setSearchObject();

} else {
    localStorage.clear();
    const today = new Date();
    const todayString = today.toISOString().substring(0, 10);

    searchObject = {
        name: "", // 노선명
        date: todayString, // 날짜
    };
    setSearchObject(); 

}

// MARK: - Today, DayBefore, DayAfter Button
const dateField = document.querySelector(".search-dispatch-path-date");
const todayButton = document.querySelector(".dispatch-path-today-button");
const dayBeforeButton = document.querySelector(".day-before-button");
const dayAfterButton = document.querySelector(".day-after-button");

const changeDateFieldValue = () => {
    setSearchObject("date", dateField.value);
}

const setToday = () => {
    const today = new Date();

    document.querySelector(".search-dispatch-path-date").value = today.toISOString().substring(0, 10);
    setSearchObject("date", today.toISOString().substring(0, 10));
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
    setSearchObject("date", yesterday.toISOString().substring(0, 10));
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

// MARK: - Search
const searchButton = document.querySelector(".dispatch-path-search-button");
const nameField = document.querySelector(".search-dispatch-path");

// variable

// function
const search = () => {
    let name = nameField.value;

    setSearchObject("name", name);
}

// eventListener
searchButton.addEventListener("click", () => {
    search();
    updateURL();
});


// MARK: - Edit Pop Up
const editButton = document.querySelector("#edit-button")
const closeButton = document.querySelector("#close-button")

const onPopUp = () => {
    document.querySelector(".pop-up-bg-container").style.display = "flex";
}

const closePopUp = () => {
    document.querySelector(".pop-up-bg-container").style.display = "none";
}

editButton.addEventListener("click", () => {
    onPopUp();
});

closeButton.addEventListener("click", () => {
    closePopUp();
})

// MARK: - Estimate Pop Up



// MARK: - 세팅
const setting = () => {
    dateField.value = getSearchObject("date");
    nameField.value = getSearchObject("name");
}

setting();
