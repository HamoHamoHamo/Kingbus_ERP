import { ClosePopup } from "/static/js/common/popupCommon.js"
import { StationDatas, Station } from "/static/js/dispatch/regularly_route/detailMapStationClass.js"

ClosePopup.addClosePopupEvent();

// closePopup.addClosePopupEvent(() => {
//     console.log("TEST", stationDatas.hasStations())
//     if (window.confirm("이 창을 닫으면 입력한 데이터가 손실됩니다. 계속하시겠습니까?")) {
//         closePopup.closePopup();
//     }
// });


const workStart = document.querySelector("#workStart")
const workStartPopup = document.querySelector("#workStartPopup")
const workEndPopup = document.querySelector("#workEndPopup")


const detailMapBtn = document.querySelector("#detailMapBtn")
const detailMapPopup = document.querySelector("#detailMapPopup")
// const addDetailMapBtn = document.querySelector(".addDetailMapBtn")
const waypointInput = document.querySelector("#waypointInput")
const detailMapTable = document.querySelector("#detailMapTable")
const saveStation = document.querySelector("#saveStation")
const popupMaplink = document.querySelector("#popupMaplink")
const deleteWaypoint = document.querySelector("#deleteWaypoint")
const stationSearchBtn = document.querySelector(".stationSearchBtn")
const stationEditDate = document.querySelector(".stationEditDate")
const editDateInput = document.querySelector(".editDateInput")

let popupCheckbox = document.querySelectorAll(".detailRoutePopupScrollBoxTbody input[type=checkbox]")
let popupAllCheckbox = document.querySelector(".detailMapPopupHeader input[type=checkbox]")

const waypointNumber = document.querySelector("#waypointNumber");
const popupDatasDiv = document.querySelector(".popupDatasDiv")

saveStation.addEventListener("click", createStationInput)

// addDetailMapBtn.addEventListener("click", addWaypoint)

detailMapBtn.addEventListener("click", openDetailMapPopup)

// 확인 클릭 시 데이터 input 생성
function createStationInput() {
    if (stationDatas.validateDatas() == false) {
        return;
    } else if (detailExist && stationEditDate.value == '') {
        window.alert("기준일을 입력해 주세요.")
        return;
    }
    // 기존 데이터 input 삭제
    popupDatasDiv.innerHTML = '';

    Array.from(stationDatas.getStationElements()).forEach(div => {
        popupDatasDiv.appendChild(div);
    })
    // 수정일 경우 기준일 값 넣기
    if (detailExist) {
        editDateInput.value = stationEditDate.value
    }
    // 정류장 개수 input 생성
    // popupDatasDiv.appendChild(stationDatas.getWaypointNumberElement());
    waypointNumber.value = stationDatas.waypointNumber;
    console.log("AA", popupDatasDiv);
    
    closeDetailMapPopup();
}

// 정류장 팝업 열기
function openDetailMapPopup() {
    detailMapPopup.style.display = "block";
    getStationListData();
    // STATION_TYPES는 regularly_route.html에서 선언
    const work_type = workStart.checked ? '출근' : '퇴근';
    // const work_type = '출근';
    if (work_type == '출근') {
        workStartPopup.checked = true;
    } else {
        workEndPopup.checked = true;
    }

    createForms(STATION_TYPES[work_type]);
    popupCheckbox = document.querySelectorAll(".detailRoutePopupScrollBoxTbody input[type=checkbox]");

    // 이미 데이터가 있으면 불러오기
    console.log("waypointNumber", waypointNumber);
    if (waypointNumber.value) {
        changeWaypointNumber(waypointNumber.value);
        waypointNumberInput.value = waypointNumber.value;
        Array.from(popupDatasDiv.children)?.forEach(div => {
            console.log("DIV", div);
            const indexNumber = div.children[0].value;
            const name = div.children[2].value;
            const time = div.children[3].value;
            const references = div.children[4].value;
            const id = div.children[5].value;
    
            // id name references indexNumber
            selectStation(id, name, references, time, Number(indexNumber) - 1);
            // indexNumber
        })
    }

}

// 정류장 목록으로 테이블 만들기
const tbody = document.querySelector(".detailMapPopupScrollBoxTbody");
const createDatas = (datas) => {
    const headers = [
        'station_type',
        'name',
        'latitude',
        'longitude',
        'address',
        'references',
    ]
    datas?.forEach((data, index) => {
        const tr = document.createElement('tr');
        tr.setAttribute('class', 'detailMapPopupScrollBoxTr')
        const indexTd = document.createElement('td');
        indexTd.textContent = index + 1;
        tr.appendChild(indexTd);

        headers.forEach(header => {
            const td = document.createElement('td');
            td.textContent = data[header];
            tr.appendChild(td);
        });
        const id = document.createElement('input')
        id.setAttribute("type", 'hidden')
        id.setAttribute("name", 'id')
        id.value = data['id']
        tr.appendChild(id)

        tr.addEventListener('click', () => selectStation(data['id'], data['name'], data['references']))
        tbody.appendChild(tr)
    })
}

function closeDetailMapPopup() {
    detailMapPopup.style.display = "none";
}

// 정류장 목록 불러오기
const getStationListData = () => {
    // 기존에 있던 데이터 다 삭제
    tbody.innerHTML = ''

    const searchData = {
        'name' : document.querySelector('.stationSearchInput').value,
        'type' : document.querySelector('.stationSearchSelect').value
    }
    $.ajax({
        url: STATION_LIST_URL,
        datatype: 'json',
        data: searchData,
        success: function (data) {
            console.log(data);
            if (data) {
                createDatas(data.data)
                return
            } else {
                alert("에러가 발생했습니다.");
                return;
            }
        },
        error: function (request, status, error) {
            console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            // ajax 처리가 결과가 에러이면 전송 여부는 false // 앞서 초기값을 false로 해 놓았지만 한번 더 선언을 한다.
        }
    });
}

stationSearchBtn.addEventListener("click", getStationListData)


// 정류장 관리

// 정류장 관리 라디오 버튼, 정류장 개수
const workRadio = document.querySelectorAll(".workRadio")
let detailRoutePopupScrollBoxTbody = document.querySelector(".detailRoutePopupScrollBoxTbody")
const waypointNumberInput = document.querySelector(".waypointNumberInput")

const stationDatas = new StationDatas()


// 정류장개수 변경
waypointNumberInput.addEventListener('change', (e) => changeWaypointNumber(e.target.value));

function changeWaypointNumber(waypointNumber) {
    const number = Number(waypointNumber);
    const type = '정류장';

    let lastWaypointIndex = getLastWaypointIndex(type);
    // 정류장 추가
    console.log("counter", number, stationDatas.waypointNumber, stationDatas.getStationsLength())
    if (number > stationDatas.waypointNumber) {
        const counter = number - Number(stationDatas.waypointNumber);
        console.log("COUNTER", counter)
        for (let i = 0; i < counter; i++) {
            const newTr = createDetailRouteTr(type, lastWaypointIndex);
            detailRoutePopupScrollBoxTbody.insertBefore(newTr, detailRoutePopupScrollBoxTbody.children[lastWaypointIndex]);
        }

        stationDatas.waypointNumber = number;
        stationDatas.index = lastWaypointIndex;
        replaceTrIndex(lastWaypointIndex);
    }
    // 정류장 삭제
    else {
        lastWaypointIndex -= 1;
        const counter = Number(stationDatas.waypointNumber) - number;
        console.log("COUNTER2", counter)
        for (let i = 0; i < counter; i++) {
            const tr = detailRoutePopupScrollBoxTbody.children[lastWaypointIndex - i];
            stationDatas.removeStationByTr(tr);
            tr.remove();
        }
        stationDatas.waypointNumber = number;
        replaceTrIndex(lastWaypointIndex);
    }

    popupCheckbox = document.querySelectorAll(".detailRoutePopupScrollBoxTbody input[type=checkbox]");
}

const getLastWaypointIndex = (type) => {
    return Array.from(detailRoutePopupScrollBoxTbody.children).reduce((lastMatch, item, index) => {
        if (item.children[2].textContent == type) {
            return index + 1;
        }
        return lastMatch;
    }, 2);
    
}

const replaceTrIndex = (lastWaypointIndex) => {
    Array.from(detailRoutePopupScrollBoxTbody.children).forEach((item, index) => {
        item.children[1].textContent = index + 1;
    })

    // station index 수정
    // stationDatas.setStationsIndex();
}

// 출근 퇴근 선택
Array.from(workRadio).map(radio => {
    radio.addEventListener('change', (e) => {
        createForms(STATION_TYPES[e.target.value])
        waypointNumberInput.value = 1;
    })
})

function createForms(types) {
    // 초기화
    detailRoutePopupScrollBoxTbody.innerHTML = ''
    stationDatas.dispose();

    types.forEach((type, index) => {
        const tr = createDetailRouteTr(type, index)
        detailRoutePopupScrollBoxTbody.appendChild(tr);
    })
    popupCheckbox = document.querySelectorAll(".detailRoutePopupScrollBoxTbody input[type=checkbox]")
}

const createDetailRouteTr = (type, index) => {
    const tr = document.createElement('tr');

    const checkboxTd = document.createElement('td');
    const checkbox = document.createElement('input');
    checkbox.setAttribute('type', 'checkbox')
    checkboxTd.appendChild(checkbox);
    tr.appendChild(checkboxTd);

    const indexTd = document.createElement('td');
    indexTd.textContent = index + 1;
    tr.appendChild(indexTd);

    const typeTd = document.createElement('td');
    typeTd.textContent = type;
    tr.appendChild(typeTd);

    tr.appendChild(document.createElement('td'));
    tr.appendChild(document.createElement('td'));
    tr.appendChild(document.createElement('td'));
    return tr
}

// 정류장 선택
const selectStation = (id, name, references, time='', indexNumber=-1) => {
    if (detailRoutePopupScrollBoxTbody.children.length <= stationDatas.getStationsLength()) return;

    console.log("indexNumber", indexNumber);
    const detailRouteTrIdIndex = 6
    if (indexNumber < 0) {
        stationDatas.setIndex(detailRoutePopupScrollBoxTbody, detailRouteTrIdIndex)
    } else {
        stationDatas.index = indexNumber;
    }

    const routeStation = detailRoutePopupScrollBoxTbody.childNodes[stationDatas.index]
    // const thisTr = e.target.parentElement
    // const stationId = thisTr.childNodes[7]

    const idInput = document.createElement('input')
    idInput.setAttribute('type', 'hidden')
    idInput.setAttribute('name', 'stationId')
    // const id = stationId.value
    idInput.value = id
    routeStation.appendChild(idInput)

    // 정류장명
    // const name = thisTr.childNodes[2].textContent
    routeStation.childNodes[3].textContent = name

    // 시각
    routeStation.childNodes[4].innerHTML = ''
    const timeInput = document.createElement('input')
    timeInput.setAttribute('type', 'time')
    timeInput.setAttribute('class', 'routeStationTime')
    timeInput.value = time
    routeStation.childNodes[4].appendChild(timeInput)
    timeInput.addEventListener('change', (event) => setDataTime(event, stationDatas))

    // 참조사항
    // const references = thisTr.childNodes[6].textContent
    routeStation.childNodes[5].textContent = references

    // 종류
    const type = routeStation.childNodes[2].textContent

    console.log("tr", routeStation)
    const station = new Station(routeStation, id, type, name, references, time)
    stationDatas.addStation(station)
}

const setDataTime = (e, stationDatas) => {
    const tr = e.target.parentElement.parentElement;
    // const index = e.target.parentElement.parentElement.children[1].textContent - 1;
    // console.log("timeindex", index)
    const station = stationDatas.getStationByTr(tr);

    station.time = e.target.value;
}

// 체크박스
for (i = 0; i < popupCheckbox.length; i++){
    popupCheckbox[i].addEventListener('change', popupDeletecheck)
};

function popupDeletecheck(e){
    e.stopPropagation()
    console.log("TEST");
    let checkCount = 0
    for (i = 0; i < popupCheckbox.length; i++){
        if(popupCheckbox[i].checked){
            checkCount++ 
        }
    };
    if(popupCheckbox.length === checkCount){
        popupAllCheckbox.checked = true
    }else{
        popupAllCheckbox.checked = false
    }
}

popupAllCheckbox.addEventListener("change", popupAllDeleteCheck)

function popupAllDeleteCheck(){
    if(this.checked){
        for (i = 0; i < popupCheckbox.length; i++){
            popupCheckbox[i].checked = true
        };
    }else{
        for (i = 0; i < popupCheckbox.length; i++){
            popupCheckbox[i].checked = false
        };
    }
}

// 체크 삭제

deleteWaypoint.addEventListener("click", deleteWaypointTr);

function deleteWaypointTr() {
    const checkedCheckboxes = document.querySelectorAll(".detailRoutePopupScrollBoxTbody input[type=checkbox]:checked");

    Array.from(checkedCheckboxes).map(checkbox => {
        const tr = checkbox.parentElement.parentElement;
        tr.children[3].innerHTML = '';
        tr.children[4].innerHTML = '';
        tr.children[5].innerHTML = '';
        tr.children[6]?.remove()

        stationDatas.removeStationByTr(tr);
        checkbox.checked = false;
    })
    popupAllCheckbox.checkd = false;
    // stationDatas.setStationsIndex();
}

// 각 정류장 시간, 거리 계산
const detailMapCalculatePopup = document.querySelector("#detailMapCalculatePopup");
const detailMapCalculatePopupOpenButton = document.querySelectorAll(".detailMapCalculatePopupOpenButton");

Array.from(detailMapCalculatePopupOpenButton)
    .forEach(button => button.addEventListener('click', () => {
        detailMapCalculatePopup.style.display = "block"
        console.log("TEST")
    })
)