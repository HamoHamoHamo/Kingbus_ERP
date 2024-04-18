function afterSelectRoute() {
    const businput = document.querySelector(".RouteListHBodyTr input[type=text]")
    const driverSelect = document.querySelector(".driverSelect")



    // 운전원 옵션

    let useSelect = true;

    // 배차가능 기사 필터(기사-옵션)
    driverSelect.addEventListener("click", addDriverOption);

    function addDriverOption() {
        const connectTime = this.parentNode.parentNode.querySelector('.connectTime')
        const departureDate = `${URL_DATE} ${connectTime.innerText.split(" ~ ")[0]}`
        const arrivalDate = `${URL_DATE} ${connectTime.innerText.split(" ~ ")[1]}`

        if (useSelect == true || useSelect !== this) {

            // 1. 선택된 기사존재여부 -> 첫번째 옵션 저장

            let firstOption = []

            if (this.children.length !== 0) {
                for (i = 0; i < this.children.length; i++) {
                    if (this.children[i].selected) {
                        firstOption.push(this.children[i].value)
                        firstOption.push(this.children[i].innerText)
                    }
                }
            } else {
                firstOption.push("")
                firstOption.push("")
            }

            // 2. this 옵션 삭제

            this.innerText = ""

            // 3. 배차불가 기사 추출 -> 기간 필터링

            let periodFilter = []

            for (i = 0; i < dataList.length; i++) {
                let dataStartTime = dataList[i].departure_date
                let dataEndTime = dataList[i].arrival_date
                
                if (dataEndTime >= departureDate && dataStartTime <= arrivalDate) {
                    periodFilter.push(`${dataList[i].driver_id}`)
                }
            }
            
            // 4. 배차가능 기사 추출 -> 기사데이터 - 3번

            let useDriver = []

            for (i = 0; i < Object.keys(driverObj).length; i++) {
                useDriver.push(Object.keys(driverObj)[i])
            }

            for (i = 0; i < periodFilter.length; i++) {
                useDriver = useDriver.filter(current => current !== periodFilter[i])
            }

            // 4-2. 배차가능 기사 추출 -> 현재 선택기사 제거
            useDriver = useDriver.filter(current => current !== firstOption[0])

            // 5. 배차가능 배열 오브젝트로 변경

            let useDriverSort = []

            for (i = 0; i < Object.keys(driverObj).length; i++) {
                for (j = 0; j < useDriver.length; j++) {
                    if (Object.keys(driverObj)[i] == useDriver[j]) {
                        let useDriveObj = {
                            name: `${Object.keys(driverObj)[i]}`,
                            driver: `${Object.values(driverObj)[i]}`
                        }
                        useDriverSort.push(useDriveObj)
                    }
                }
            }

            // 6. 배차가능 오브젝트 정렬

            useDriverSort.sort(function (a, b) {
                return a.driver < b.driver ? -1 : a.driver > b.driver ? 1 : 0;
            });

            // 7. 첫번째 옵션 생성 -> 1번

            const driverOption = document.createElement('option');
            driverOption.setAttribute("value", `${firstOption[0]}`);
            driverOption.innerText = `${firstOption[1]}`
            this.appendChild(driverOption);

            // 8. 선택가능 기사 옵션 생성 -> 5번

            for (i = 0; i < useDriverSort.length; i++) {
                const driverOption = document.createElement('option');
                driverOption.setAttribute("value", `${useDriverSort[i].name}`);
                driverOption.innerText = `${useDriverSort[i].driver}`
                this.appendChild(driverOption);
            }

            useSelect = this
        } else {
            useSelect = true
        }
    }
}