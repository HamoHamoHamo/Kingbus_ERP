import { StationDatas, Station } from "/static/js/dispatch/order/stationSearchClass.js"

const searchInput = document.querySelector(".stationSearchInput");
const searchButton = document.querySelector(".stationSearchButton");
const stationSearchResultBox = document.querySelector(".stationSearchResultBox");
const stationSearchLoadingBox = document.querySelector(".stationSearchLoadingBox");
const stationPopupBody = document.querySelector(".stationPopupBody");

stationPopupBody.addEventListener('click', (event) => {
    if (event.target === searchInput && stationDatas.page > 1 || searchButton === event.target) {
        stationSearchResultBox.style.display = "block"
    }
    else {
        stationSearchResultBox.style.display = "none"
    }
    // console.log("click", event.target, event.currentTarget)
})

searchButton.addEventListener("click", onClickSearch)

let stationDatas = new StationDatas()

// 장소 검색
function onClickSearch() {
    if (!(searchInput.value)) {
        alert("검색할 장소를 입력해 주세요.")
        return
    }
    resetSearchStations();
    stationSearchResultBox.style.display = "block"
    stationSearchLoadingBox.style.display = "flex"
    searchStation(searchInput.value, stationDatas.page);
    console.log('station', stationDatas)
}

function setStationDatas(data) {
    data.data.documents?.map((info) => {
        // console.log("TEST", info)
        const station = new Station(
            info.address_name,
            info.place_name,
            info.x,
            info.y,
        )
        stationDatas.addStation(station)
    })
    if (data.data.documents) stationDatas.countPage();
}

// 선택한 장소 정보로 위도, 경도, 장소명, 주소 채우기
function onClickInfoBox(e) {
    console.log("E", e)
    const infoBox = e.currentTarget
    console.log("infoBox", infoBox, infoBox.childNode)
    inputPlace.textContent = infoBox.querySelector('.stationName').textContent
    inputAddress.textContent = infoBox.querySelector('.stationAddress').textContent
    inputLatitude.textContent = infoBox.querySelector('.stationLatitude').textContent
    inputLongitude.textContent = infoBox.querySelector('.stationLongitude').textContent

}

// 검색 결과 만들기
function createSearchInfoBox(data) {
    stationSearchLoadingBox.style.display = 'none'
    
    data.data.documents?.map(info => {
        const infoBox = document.createElement('div')
        infoBox.setAttribute('class', 'stationSearchInfoBox')
        infoBox.addEventListener('click', onClickInfoBox)
        
        const name = document.createElement('div')
        name.textContent = info.place_name
        name.setAttribute('class', 'stationName')
    
        const address = document.createElement('div')
        address.textContent = info.address_name
        address.setAttribute('class', 'stationAddress')

        const latitude = document.createElement('div')
        latitude.textContent = info.y
        latitude.style.display = 'none'
        latitude.setAttribute('class', 'stationLatitude')

        const longitude = document.createElement('div')
        longitude.textContent = info.x
        longitude.style.display = 'none'
        longitude.setAttribute('class', 'stationLongitude')

        infoBox.appendChild(name)
        infoBox.appendChild(address)
        infoBox.appendChild(longitude)
        infoBox.appendChild(latitude)
    
        stationSearchResultBox.appendChild(infoBox)
    })
    
    // console.log("STTATTION", stationDatas)
}

function searchStation(query, page) {
    $.ajax({
        url: STATION_SEARCH_URL,
        method: "POST",
        data: JSON.stringify({
            'query' : query,
            'page' : page,
        }),
        datatype: 'json',
        success: function (data) {
            // visibleLoading.style.display = "none"
            uploadState = true
            console.log("API DATA", data)
            if (data['result'] == 'true') {
                console.log("success data", data);
                setStationDatas(data);
                createSearchInfoBox(data);

            } else if (data.data.meta.pageable_count === 0) {
                console.log("ERROR", data);
                stationSearchResultBox.style.display = "none"
                stationSearchLoadingBox.style.display = "none"
                alert('검색 결과가 없습니다.');
            } else {
                console.log("ERROR", data);
                alert('에러 발생\n' + data.meta.pagea);
                stationSearchResultBox.style.display = "none"
                stationSearchLoadingBox.style.display = "none"
            }
            // excelUploadFile.value = ""
            // excelUploadFileText.value = ""
            // uploadState = true;
            return
        },
        error: function (request, status, error) {
            alert("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
        },
    });
}

stationSearchResultBox.addEventListener('scroll', onScroll)
let blockApi = false

function onScroll(e) {
    // 스크롤 최대한 내렸을 때 stationSearchResultBox.scrollHeight - e.target.scrollTop = 155
    if (stationSearchResultBox.scrollHeight - e.target.scrollTop < 180) {
        console.log("TEST", stationSearchResultBox.scrollHeight - e.target.scrollTop)
        blockApi = true

    }
}

function resetSearchStations() {
    stationDatas.resetDatas();
    
    const allStationSearchInfoBox = document.querySelectorAll('.stationSearchInfoBox')
    allStationSearchInfoBox.forEach(item => item.remove());
}


// station.js

const popupAreaModules = document.querySelectorAll('.popupAreaModules');
const popupBgModules = document.querySelectorAll(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const stationCloseBtn = document.querySelector(".stationCloseBtn")
const stationInput = document.querySelector(".stationInput")
const stationTimeInput = document.querySelector(".stationTimeInput")
const delegateInput = document.querySelector(".delegateInput")
const delegatePhoneInput = document.querySelector(".delegatePhoneInput")
const addWaypointBtn = document.querySelector(".addWaypointBtn")
const createTable = document.querySelector(".stationTable tbody")
const stationDeleteBtn = document.querySelector(".stationDeleteBtn")
const addtionalBtn = document.querySelector(".addtionalBtn")
const openStationPopupBtn = document.querySelectorAll(".openStationPopupBtn")

openStationPopupBtn.forEach(item => item.addEventListener("click", openStationPopup))


function openStationPopup() {
    popupAreaModules[1].style.display = "block"
}

popupBgModules[1].addEventListener("click", closeWaypointPopup)
SidemenuUseClose.addEventListener("click", closeWaypointPopup)
stationCloseBtn.addEventListener("click", closeWaypointPopup)

function closeWaypointPopup() {
    popupAreaModules[1].style.display = "none"
    resetSearchStations()
    resetInput()
}

stationTimeInput.addEventListener("input", maxlength)

function maxlength() {
    if (stationTimeInput.value.length >= 4) {
        stationTimeInput.value = stationTimeInput.value.substr(0, 4)
    }
}

delegatePhoneInput.addEventListener("input", maxlengthPhone)

function maxlengthPhone() {
    if (delegatePhoneInput.value.length >= 11) {
        delegatePhoneInput.value = delegatePhoneInput.value.substr(0, 11)
    }
}

addWaypointBtn.addEventListener("click", createWaypoint)

const inputPlace = document.querySelector(".inputPlace")
const inputAddress = document.querySelector(".inputAddress")
const inputLatitude = document.querySelector(".inputLatitude")
const inputLongitude = document.querySelector(".inputLongitude")

function createWaypoint() {
    console.log(stationTimeInput.value.length !== 4 && stationTimeInput.value.length !== 0)
    if (stationInput.value == "") {
        alert("정류장명을 입력해 주세요.")
    } else if (inputPlace.textContent == '' || 
        inputAddress.textContent == '' ||
        inputLatitude.textContent == '' ||
        inputLongitude.textContent == ''
    ) {
        alert("장소를 검색하여 선택해 주세요.")
    } else {
        const stationTr = document.createElement("tr")
        stationTr.setAttribute("class", "table-list_body-tr")
        createTable.appendChild(stationTr);

        const stationTd1 = document.createElement("td")
        stationTd1.setAttribute("class", "table-list_body-tr_td")
        stationTr.appendChild(stationTd1);

        const stationCheckbox = document.createElement("input")
        stationCheckbox.setAttribute("type", "checkbox")
        stationCheckbox.setAttribute("calss", "stationCheckbox")
        stationTd1.appendChild(stationCheckbox);

        const stationTd2 = document.createElement("td")
        stationTd2.setAttribute("class", "table-list_body-tr_td")
        stationTd2.innerText = stationInput.value
        stationTr.appendChild(stationTd2);


        const stationTd3 = document.createElement("td")
        stationTd3.setAttribute("class", "table-list_body-tr_td")
        stationTd3.innerText = `${stationTimeInput.value = stationTimeInput.value.replace(/^(\d{2})(\d{2})$/, `$1:$2`)}`
        stationTr.appendChild(stationTd3);


        const stationTd4 = document.createElement("td")
        stationTd4.setAttribute("class", "table-list_body-tr_td")
        stationTd4.innerText = delegateInput.value
        stationTr.appendChild(stationTd4);


        const stationTd5 = document.createElement("td")
        stationTd5.setAttribute("class", "table-list_body-tr_td")
        stationTd5.innerText = `${delegatePhoneInput.value = delegatePhoneInput.value.replace(/^(\d{2,3})(\d{3,4})(\d{4})$/, `$1-$2-$3`)}`
        stationTr.appendChild(stationTd5);

        
        stationTr.appendChild(createTableTd('table-list_body-tr_td tablePlace', inputPlace.textContent));
        stationTr.appendChild(createTableTd('table-list_body-tr_td tableAddres', inputAddress.textContent));
        stationTr.appendChild(createTableDiv('tableLatitude', inputLatitude.textContent));
        stationTr.appendChild(createTableDiv('tableLongitude', inputLongitude.textContent));
        
        // 추가하면 입력된 값 지우기
        resetInput()
    }
}

function resetInput() {
    stationInput.value = ""
    stationTimeInput.value = ""
    delegateInput.value = ""
    delegatePhoneInput.value = ""
    inputPlace.textContent = ""
    inputAddress.textContent = ""
    inputLatitude.textContent = ""
    inputLongitude.textContent = ""
    searchInput.value = ""
}


function createTableDiv(className, text) {
    const div = document.createElement("div")
    div.setAttribute("class", className)
    div.style.display = 'none';
    div.innerText = text
    
    return div
}

function createTableTd(className, text) {
    const td = document.createElement("td")
    td.setAttribute("class", className)
    td.innerText = text
    
    return td
}

createTable.addEventListener("mouseover", find)

function find() {
    for (i = 0; i < this.children.length; i++) {
        this.children[i].children[0].children[0].addEventListener("change", checkedWaypoint)
    };
}

function checkedWaypoint() {
    if (this.checked) {
        this.parentNode.parentNode.classList.add("checking")
    } else if (this.checked == false && this.parentNode.parentNode.classList.contains("checking")) {
        this.parentNode.parentNode.classList.remove("checking")
    }
}

stationDeleteBtn.addEventListener("click", deleteWaypoint)

function deleteWaypoint() {
    const checkingWaypoint = document.querySelectorAll(".checking")
    for (i = 0; i < checkingWaypoint.length; i++) {
        checkingWaypoint[i].remove()
    };
}


const inputDeparture = document.querySelector('.inputDeparture')
const inputArrival = document.querySelector('.inputArrival')

addtionalBtn.addEventListener("click", additionalWaypoint)

function additionalWaypoint() {

    const hiddenWaypoint = document.querySelectorAll("input[name=station_name]")
    const stationTimeHidden = document.querySelectorAll("input[name=station_time]")
    const delegateHidden = document.querySelectorAll("input[name=delegate]")
    const delegatePhoneHidden = document.querySelectorAll("input[name=delegate_phone]")
    const placeHidden = document.querySelectorAll("input[name=place_name]")
    const addressHidden = document.querySelectorAll("input[name=address]")
    const longitudeHidden = document.querySelectorAll("input[name=longitude]")
    const latitudeHidden = document.querySelectorAll("input[name=latitude]")

    hiddenWaypoint.forEach(item => item.remove());
    stationTimeHidden.forEach(item => item.remove());
    delegateHidden.forEach(item => item.remove());
    delegatePhoneHidden.forEach(item => item.remove());
    placeHidden.forEach(item => item.remove());
    addressHidden.forEach(item => item.remove());
    longitudeHidden.forEach(item => item.remove());
    latitudeHidden.forEach(item => item.remove());
    
    if (createTable.children.length >= 2) {
        for (i = 0; i < createTable.children.length; i++) {
            inputDispatchForm.appendChild(createHiddenInput("station_name", createTable.children[i].children[1].innerText));
            inputDispatchForm.appendChild(createHiddenInput("station_time", createTable.children[i].children[2].innerText));
            inputDispatchForm.appendChild(createHiddenInput("delegate", createTable.children[i].children[3].innerText));
            inputDispatchForm.appendChild(createHiddenInput("delegate_phone", createTable.children[i].children[4].innerText));
            inputDispatchForm.appendChild(createHiddenInput("place_name", createTable.children[i].children[5].innerText));
            inputDispatchForm.appendChild(createHiddenInput("address", createTable.children[i].children[6].innerText));
            inputDispatchForm.appendChild(createHiddenInput("latitude", createTable.children[i].children[7].innerText));
            inputDispatchForm.appendChild(createHiddenInput("longitude", createTable.children[i].children[8].innerText));

            if (i === 0) {
                inputDeparture.value = createTable.children[i].children[1].innerText
            } else if (i === createTable.children.length - 1) {
                inputArrival.value = createTable.children[i].children[1].innerText
            }
        };
    } else {
        alert("정류장을 2개 이상 입력해 주세요.")
        return
    }
    // 팝업 닫기
    popupAreaModules[1].style.display = "none"
}

function createHiddenInput(name, value) {
    const hiddenInput = document.createElement("input")
    hiddenInput.setAttribute("type", "hidden")
    hiddenInput.setAttribute("name", name)
    hiddenInput.setAttribute("value", value)

    return hiddenInput
}

// 예상시간, 거리 팝업
const openTimeDistancePopupBtn = document.querySelectorAll('.openTimeDistancePopupBtn')
const timeDistancePopupCloseBtn = document.querySelector('.timeDistancePopupCloseBtn')


openTimeDistancePopupBtn.forEach(item => item.addEventListener("click", openTimeDistancePopup))

function openTimeDistancePopup(e) {
    popupAreaModules[5].style.display = 'block';
}

popupBgModules[5].addEventListener("click", closeTimeDistancePopup)
SidemenuUseClose.addEventListener("click", closeTimeDistancePopup)
timeDistancePopupCloseBtn.addEventListener("click", closeTimeDistancePopup)

function closeTimeDistancePopup() {
    popupAreaModules[5].style.display = "none"
}