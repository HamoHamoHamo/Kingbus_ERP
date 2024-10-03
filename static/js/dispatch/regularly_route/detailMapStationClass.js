class StationDatas {
    #index = 0;
    #stations = [];
    #waypointNumber = 1;

    dispose() {
        // 각 Station 객체의 dispose 메서드를 호출하여 내부 리소스를 해제
        this.#stations.forEach(station => {
            if (station.dispose) {
                station.dispose();
            }
        });
        // #stations 배열 초기화
        this.#stations = [];
        this.#index = 0;
        this.#waypointNumber = 1;
    }

    addStation(station) {
        this.#stations.splice(this.#index, 0, station);
        console.log("station", this.#stations);
        // this.setStationsIndex();
    }

    setIndex(tbody, idIndex) {
        const tr = tbody.children;
        for (let i = 0; i < tr.length; i++) {
            if (tr[i].children[idIndex] == undefined) {
                console.log("iNDEx", i);
                this.#index = i;
                break;
            }
        }
    }

    getStationByTr(tr) {
        return this.#stations.find(station => station.tr == tr);
    }

    getStationsLength() {
        return this.#stations.length;
    }

    removeStationByTr(tr) {
        this.#stations.forEach((station, i) => {
            if (station.tr == tr) {
                console.log("statoins", this.#stations)
                this.#stations.splice(i, 1);
            }
        })
    }

    getStationElements() {
        return this.#stations.map(station => station.getElement());
    }

    hasStations = () => this.#stations.length > 0 ? true : false;

    validateDatas = () => {
        return this.validateTime() && this.validateWaypointNumber() && this.validateLength();
    }

    validateLength = () => {
        console.log("LENGTH", this.#stations.length, this.#waypointNumber)
        if (this.#stations.length < 7 + this.#waypointNumber) {
            window.alert('정류장을 모두 입력해 주세요.');
            return false;
        }
        return true;
    }

    validateTime() {
        return this.#stations.every(station => {
            if (station.time == '') {
                window.alert('시각을 입력해 주세요.');
                return false;
            }
            return true;
        })
    }

    validateWaypointNumber = () => {
        const number = this.#stations.filter(station => station.type == '정류장').length;
        if (number != this.#waypointNumber) {
            window.alert("정류장 개수에 맞게 입력해 주세요.")
            console.log("TEST", number, this.#waypointNumber);
            return false;
        }
        return true;
    }

    getWaypointNumberElement() {
        const input = document.createElement('input');
        input.setAttribute("value", this.#waypointNumber);
        input.setAttribute("type", 'hidden');
        input.setAttribute("id", 'waypointNumber');
        return input;
    }

    get index() {
        return this.#index;
    }

    set index(i) {
        this.#index = i;
    }
    
    get waypointNumber() {
        return this.#waypointNumber;
    }

    set waypointNumber(number) {
        if (Number(number) == NaN) {
            console.error("타입 에러 발생: ", number);
        } else {
            this.#waypointNumber = Number(number);
        }
    }

}

class Station {
    time = '';

    constructor(tr, id, type, name, references, time='') {
        this.tr = tr;
        this.id = id;
        this.type = type;
        this.name = name;
        this.references = references;
        this.time = time;
    }

    set time(time) {
        this.time = time;
    }

    dispose() {
        // Station 객체의 내부 리소스 해제
        this.tr = null;
        this.time = null;
        this.id = null;
        this.type = null;
        this.name = null;
        this.references = null;
    }

    getIndex() {
        return this.tr.children[1].textContent;
    }

    getElement() {
        const div = document.createElement('div');
        div.appendChild(this.createHiddenInput(this.getIndex(), 'station_index'));
        div.appendChild(this.createHiddenInput(this.type, 'station_type'));
        div.appendChild(this.createHiddenInput(this.name, 'station_name'));
        div.appendChild(this.createHiddenInput(this.time, 'station_time'));
        div.appendChild(this.createHiddenInput(this.references, 'station_references'));
        div.appendChild(this.createHiddenInput(this.id, 'station_id'));
        return div;
    }

    createHiddenInput(value, name) {
        const input = document.createElement('input');
        input.setAttribute('type', 'hidden');
        input.setAttribute('value', value);
        input.setAttribute('name', name);
        return input;
    }
}

export { StationDatas, Station };