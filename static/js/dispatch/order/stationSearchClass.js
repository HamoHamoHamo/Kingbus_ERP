class StationDatas {
    #stations
    #count
    #page
    #isEnd

    constructor() {
        this.resetDatas();
    }

    resetDatas() {
        this.#stations = [];
        this.#count = 0;
        this.#page = 1;
        this.#isEnd = false;
    }

    addStation(station) {
        this.#stations.push(station);
        this.#count += 1;
    }

    countPage() {
        this.#page += 1;
    }

    get count() {
        return this.#count;
    }

    get page() {
        return this.#page;
    }
}

class Station {
    constructor(address, place, longitude, latitude) {
        this.address = address;
        this.place = place;
        this.longitude = longitude;
        this.latitude = latitude;
    }
}

export { StationDatas, Station };