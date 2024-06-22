const waypoinBtn = document.querySelector(".waypoinBtn")
const popupAreaModules = document.querySelectorAll('.popupAreaModules');
const popupBgModules = document.querySelectorAll(".popupBgModules")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const waypointCloseBtn = document.querySelector(".waypointCloseBtn")
const waypointInput = document.querySelector(".waypointInput")
const waypointTimeInput = document.querySelector(".waypointTimeInput")
const delegateInput = document.querySelector(".delegateInput")
const delegatePhoneInput = document.querySelector(".delegatePhoneInput")
const addWaypointBtn = document.querySelector(".addWaypointBtn")
const createTable = document.querySelector(".waypointTable tbody")
const waypointDeleteBtn = document.querySelector(".waypointDeleteBtn")
const addtionalBtn = document.querySelector(".addtionalBtn")

waypoinBtn.addEventListener("click", openWaypointPopup)

function openWaypointPopup() {
    popupAreaModules[1].style.display = "block"
}

popupBgModules[1].addEventListener("click", closeWaypointPopup)
SidemenuUseClose.addEventListener("click", closeWaypointPopup)
waypointCloseBtn.addEventListener("click", closeWaypointPopup)

function closeWaypointPopup() {
    popupAreaModules[1].style.display = "none"

}

waypointTimeInput.addEventListener("input", maxlength)

function maxlength() {
    if (waypointTimeInput.value.length >= 4) {
        waypointTimeInput.value = waypointTimeInput.value.substr(0, 4)
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
    console.log(waypointTimeInput.value.length !== 4 && waypointTimeInput.value.length !== 0)
    if (waypointInput.value == "") {
        alert("정류장명을 입력해 주세요.")
    } else if (inputPlace.textContent == '' || 
        inputAddress.textContent == '' ||
        inputLatitude.textContent == '' ||
        inputLongitude.textContent == ''
    ) {
        alert("장소를 검색하여 선택해 주세요.")
    } else {
        const waypointTr = document.createElement("tr")
        waypointTr.setAttribute("class", "table-list_body-tr")
        createTable.appendChild(waypointTr);

        const waypointTd1 = document.createElement("td")
        waypointTd1.setAttribute("class", "table-list_body-tr_td")
        waypointTr.appendChild(waypointTd1);

        const waypointCheckbox = document.createElement("input")
        waypointCheckbox.setAttribute("type", "checkbox")
        waypointCheckbox.setAttribute("calss", "waypointCheckbox")
        waypointTd1.appendChild(waypointCheckbox);

        const waypointTd2 = document.createElement("td")
        waypointTd2.setAttribute("class", "table-list_body-tr_td")
        waypointTd2.innerText = waypointInput.value
        waypointTr.appendChild(waypointTd2);


        const waypointTd3 = document.createElement("td")
        waypointTd3.setAttribute("class", "table-list_body-tr_td")
        waypointTd3.innerText = `${waypointTimeInput.value = waypointTimeInput.value.replace(/^(\d{2})(\d{2})$/, `$1:$2`)}`
        waypointTr.appendChild(waypointTd3);


        const waypointTd4 = document.createElement("td")
        waypointTd4.setAttribute("class", "table-list_body-tr_td")
        waypointTd4.innerText = delegateInput.value
        waypointTr.appendChild(waypointTd4);


        const waypointTd5 = document.createElement("td")
        waypointTd5.setAttribute("class", "table-list_body-tr_td")
        waypointTd5.innerText = `${delegatePhoneInput.value = delegatePhoneInput.value.replace(/^(\d{2,3})(\d{3,4})(\d{4})$/, `$1-$2-$3`)}`
        waypointTr.appendChild(waypointTd5);

        
        waypointTr.appendChild(createTableTd('tablePlace', inputPlace.textContent));
        waypointTr.appendChild(createTableTd('tableAddres', inputAddress.textContent));
        waypointTr.appendChild(createTableDiv('tableLatitude', inputLatitude.textContent));
        waypointTr.appendChild(createTableDiv('tableLongitude', inputLongitude.textContent));
        
        // 추가하면 입력된 값 지우기
        waypointInput.value = ""
        waypointTimeInput.value = ""
        delegateInput.value = ""
        delegatePhoneInput.value = ""
        inputPlace.textContent = ""
        inputAddress.textContent = ""
        inputLatitude.textContent = ""
        inputLongitude.textContent = ""

    }
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
    td.setAttribute("class", `${table-list_body-tr_td} ${className}`)
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

waypointDeleteBtn.addEventListener("click", deleteWaypoint)

function deleteWaypoint() {
    const checkingWaypoint = document.querySelectorAll(".checking")
    for (i = 0; i < checkingWaypoint.length; i++) {
        checkingWaypoint[i].remove()
    };
}


addtionalBtn.addEventListener("click", additionalWaypoint)

function additionalWaypoint() {

    const hiddenWaypoint = document.querySelectorAll("input[name=waypoint]")
    const waypointTimeHidden = document.querySelectorAll("input[name=waypoint_time]")
    const delegateHidden = document.querySelectorAll("input[name=delegate]")
    const delegatePhoneHidden = document.querySelectorAll("input[name=delegate_phone]")
    const placeHidden = document.querySelectorAll("input[name=place_name]")
    const addressHidden = document.querySelectorAll("input[name=address]")
    const longitudeHidden = document.querySelectorAll("input[name=longitude]")
    const latitudeHidden = document.querySelectorAll("input[name=latitude]")

    hiddenWaypoint.forEach(item => item.remove());
    waypointTimeHidden.forEach(item => item.remove());
    delegateHidden.forEach(item => item.remove());
    delegatePhoneHidden.forEach(item => item.remove());
    placeHidden.forEach(item => item.remove());
    addressHidden.forEach(item => item.remove());
    longitudeHidden.forEach(item => item.remove());
    latitudeHidden.forEach(item => item.remove());
    
    if (createTable.children.length >= 1) {
        for (i = 0; i < createTable.children.length; i++) {
            inputDispatchForm.appendChild(createHiddenInput("waypoint", createTable.children[i].children[1].innerText));
            inputDispatchForm.appendChild(createHiddenInput("waypoint_time", createTable.children[i].children[2].innerText));
            inputDispatchForm.appendChild(createHiddenInput("delegate", createTable.children[i].children[3].innerText));
            inputDispatchForm.appendChild(createHiddenInput("waypoint", createTable.children[i].children[4].innerText));
            inputDispatchForm.appendChild(createHiddenInput("place_name", createTable.children[i].children[5].innerText));
            inputDispatchForm.appendChild(createHiddenInput("address", createTable.children[i].children[6].innerText));
            inputDispatchForm.appendChild(createHiddenInput("latitude", createTable.children[i].children[7].innerText));
            inputDispatchForm.appendChild(createHiddenInput("longitude", createTable.children[i].children[8].innerText));
        };
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