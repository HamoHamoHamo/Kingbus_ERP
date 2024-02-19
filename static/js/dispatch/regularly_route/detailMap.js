const detailMapBtn = document.querySelector("#detailMapBtn")
const detailMapPopup = document.querySelector("#detailMapPopup")
const addDetailMapBtn = document.querySelector(".addDetailMapBtn")
const waypointInput = document.querySelector("#waypointInput")
const detailMapTable = document.querySelector("#detailMapTable")
const saveWaypoint = document.querySelector("#saveWaypoint")
const popupMaplink = document.querySelector("#popupMaplink")
const deleteWaypoint = document.querySelector("#deleteWaypoint")

deleteWaypoint.addEventListener("click", deleteWaypointTr)

saveWaypoint.addEventListener("click", makeWaypointInput)

addDetailMapBtn.addEventListener("click", addWaypoint)

detailMapBtn.addEventListener("click", opendetailMapPopup)

function deleteWaypointTr() {
    for (i=0; i<popupCheckbox.length; i++) {
        if (popupCheckbox[i].checked == true) {
            popupCheckbox[i].parentElement.parentElement.remove();
        }
    }
    for (i=0; i<detailMapTable.children.length; i++) {
        console.log("TEST", detailMapTable.children[i]);
        detailMapTable.children[i].children[1].innerText = i + 1;
    }
}

function makeWaypointInput() {
    closeDetailMapPopup();
    const waypointHidden = document.querySelectorAll(".waypointHidden")
    for (i=0; i<waypointHidden.length; i++) {
        waypointHidden[i].remove();
    }
    const detailMapInput = document.createElement("input");
    detailMapInput.setAttribute("class", "waypointHidden");
    detailMapInput.setAttribute("name", "maplink");
    detailMapInput.setAttribute("type", "hidden");
    detailMapInput.value = popupMaplink.value;
    crateRouteForm.appendChild(detailMapInput);

    for (i=0; i<detailMapTable.childElementCount; i++)
    {
        const waypointFormInput = document.createElement("input");
        waypointFormInput.setAttribute("class", "waypointHidden");
        waypointFormInput.setAttribute("name", "waypoint");
        waypointFormInput.setAttribute("type", "hidden");
        waypointFormInput.value = detailMapTable.children[i].children[2].innerText;
        
        crateRouteForm.appendChild(waypointFormInput);
    }
}

function addWaypoint() {
    if (!waypointInput.value) {
        window.alert('경유지명을 입력하세요');
        return
    }
    const waypointTr = document.createElement("tr");
    const waypointTd1 = document.createElement("td");
    const waypointCheck = document.createElement("input");
    waypointCheck.setAttribute('type', 'checkbox');
    const waypointTd2 = document.createElement("td");
    const waypointTd3 = document.createElement("td");
    
    waypointTd2.innerText = detailMapTable.childElementCount + 1;
    waypointTd3.innerText = waypointInput.value;
    
    waypointTd1.appendChild(waypointCheck);
    waypointTr.append(waypointTd1, waypointTd2, waypointTd3);
    detailMapTable.appendChild(waypointTr);
    waypointInput.value = '';
    popupCheckbox = document.querySelectorAll(".detailMapPopupScrollBox input[type=checkbox]")
}

function opendetailMapPopup() {
    detailMapPopup.style.display = "block"
}



function closeDetailMapPopup() {
    detailMapPopup.style.display = "none";
}

