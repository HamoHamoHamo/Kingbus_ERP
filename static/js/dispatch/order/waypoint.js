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

function createWaypoint() {
    console.log(waypointTimeInput.value.length !== 4 && waypointTimeInput.value.length !== 0)
    if (waypointInput.value == "") {
        alert("경유지를 입력해 주세요")
    } else {
        const waypointTr = document.createElement("tr")
        waypointTr.setAttribute("class", "table-list_body-tr")
        createTable.appendChild(waypointTr);

        const waypointtd1 = document.createElement("td")
        waypointtd1.setAttribute("class", "table-list_body-tr_td")
        waypointTr.appendChild(waypointtd1);

        const waypointCheckbox = document.createElement("input")
        waypointCheckbox.setAttribute("type", "checkbox")
        waypointCheckbox.setAttribute("calss", "waypointCheckbox")
        waypointtd1.appendChild(waypointCheckbox);

        const waypointtd2 = document.createElement("td")
        waypointtd2.setAttribute("class", "table-list_body-tr_td")
        waypointtd2.innerText = waypointInput.value
        waypointTr.appendChild(waypointtd2);


        const waypointtd3 = document.createElement("td")
        waypointtd3.setAttribute("class", "table-list_body-tr_td")
        waypointtd3.innerText = `${waypointTimeInput.value = waypointTimeInput.value.replace(/^(\d{2})(\d{2})$/, `$1:$2`)}`
        waypointTr.appendChild(waypointtd3);


        const waypointtd4 = document.createElement("td")
        waypointtd4.setAttribute("class", "table-list_body-tr_td")
        waypointtd4.innerText = delegateInput.value
        waypointTr.appendChild(waypointtd4);


        const waypointtd5 = document.createElement("td")
        waypointtd5.setAttribute("class", "table-list_body-tr_td")
        waypointtd5.innerText = `${delegatePhoneInput.value = delegatePhoneInput.value.replace(/^(\d{2,3})(\d{3,4})(\d{4})$/, `$1-$2-$3`)}`
        waypointTr.appendChild(waypointtd5);

        waypointInput.value = ""
        waypointTimeInput.value = ""
        delegateInput.value = ""
        delegatePhoneInput.value = ""
    }
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

    for (i = 0; i < hiddenWaypoint.length; i++) {
        hiddenWaypoint[i].remove()
    };
    for (i = 0; i < waypointTimeHidden.length; i++) {
        waypointTimeHidden[i].remove()
    };
    for (i = 0; i < delegateHidden.length; i++) {
        delegateHidden[i].remove()
    };
    for (i = 0; i < delegatePhoneHidden.length; i++) {
        delegatePhoneHidden[i].remove()
    };


    if (createTable.children.length >= 1) {
        for (i = 0; i < createTable.children.length; i++) {

            const waypointHidden = document.createElement("input")
            waypointHidden.setAttribute("type", "hidden")
            waypointHidden.setAttribute("name", "waypoint")
            waypointHidden.setAttribute("value", createTable.children[i].children[1].innerText)
            inputDispatchForm.appendChild(waypointHidden);

            const waypointTimeHidden = document.createElement("input")
            waypointTimeHidden.setAttribute("type", "hidden")
            waypointTimeHidden.setAttribute("name", "waypoint_time")
            waypointTimeHidden.setAttribute("value", createTable.children[i].children[2].innerText)
            inputDispatchForm.appendChild(waypointTimeHidden);

            const delegateHidden = document.createElement("input")
            delegateHidden.setAttribute("type", "hidden")
            delegateHidden.setAttribute("name", "delegate")
            if (createTable.children[i].children[3].innerText == "") {
                delegateHidden.setAttribute("value", " ")
            } else {
                delegateHidden.setAttribute("value", createTable.children[i].children[3].innerText)
            }
            inputDispatchForm.appendChild(delegateHidden);

            const delegatePhoneHidden = document.createElement("input")
            delegatePhoneHidden.setAttribute("type", "hidden")
            delegatePhoneHidden.setAttribute("name", "delegate_phone")
            if (createTable.children[i].children[4].innerText == "") {
                delegatePhoneHidden.setAttribute("value", " ")
            } else {
                delegatePhoneHidden.setAttribute("value", createTable.children[i].children[4].innerText)
            }
            inputDispatchForm.appendChild(delegatePhoneHidden);
        };
    }
    closeWaypointPopup()
    alert("경유지가 저장되었습니다.")
}