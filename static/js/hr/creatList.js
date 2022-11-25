const tbody = document.querySelector(".table-list tbody")
const pagenationBox = document.querySelector(".pagenation-numbering-box")
const prevBtn = document.querySelector(".prev_btn")
const nextBtn = document.querySelector(".next_btn")
const ageCheckbox = document.querySelector("#ageFilter")
const filterHeader = document.querySelector(".table-list_head-tr td:nth-child(5)")
const filterHeaderArrow = document.querySelector(".option-order")

let filter = false

drawMember()

function drawMember() {

    let pageParms = new URLSearchParams(location.search)

    if (pageParms.has("age")) {
        makeAgeData()
        ageCheckbox.checked = true
        if (pageParms.get("filter") == "up") {
            makeSortUpData(data)
        } else if (pageParms.get("filter") == "down") {
            makeSortDownData(data)
        }
    } else {
        data = regDatas
        if (pageParms.get("filter") == "up") {
            makeSortUpData(data)
        } else if (pageParms.get("filter") == "down") {
            makeSortDownData(data)
        }
    }

    if (pageParms.has("page")) {
        pageData = pageParms.get("page")
    } else {
        pageData = 1
    }


    let startPoint = ""

    if (pageData !== 1) {
        startPoint = (pageData - 1) * 10
    } else {
        startPoint = 0
    }

    let endPoint = ""

    if (data.length <= 10) {
        endPoint = data.length
    } else if (data.length > 10 && pageParms.get("page") == Math.ceil(data.length / 10)) {
        endPoint = 10 * (pageParms.get("page") - 1) + (data.length - (10 * (pageParms.get("page") - 1)))
    } else {
        if (pageParms.has("page")) {
            endPoint = 10 * pageParms.get("page")
        } else {
            endPoint = 10
        }
    }


    for (i = startPoint; i < endPoint; i++) {
        const memberList = document.createElement('tr');
        memberList.setAttribute("class", `table-list_body-tr member-height`);
        tbody.appendChild(memberList);

        const memberData1 = document.createElement('td');
        memberData1.setAttribute("class", `table-list_body-tr_td`);
        memberList.appendChild(memberData1);

        const memberData1Checkbox = document.createElement('input');
        memberData1Checkbox.setAttribute("type", `checkbox`);
        memberData1Checkbox.setAttribute("name", `delete_check`);
        memberData1Checkbox.setAttribute("value", `${data[i].user_id}`);
        memberData1.appendChild(memberData1Checkbox);

        const memberData2 = document.createElement('td');
        memberData2.setAttribute("class", `table-list_body-tr_td`);
        memberData2.innerText = i + 1
        memberList.appendChild(memberData2);

        const memberData3 = document.createElement('td');
        memberData3.setAttribute("class", `table-list_body-tr_td`);
        memberData3.setAttribute("onclick", `openDetailPopup(${data[i].user_id})`);
        memberData3.innerText = data[i].name
        memberList.appendChild(memberData3);

        let now = new Date();
        let year = now.getFullYear();
        var month = now.getMonth() + 1;
        var date = now.getDate();
        let ageResult = ""
        if (data[i].birthdate.substr(4, 2) < month) {
            ageResult = `${year - data[i].birthdate.substr(0, 4) + 1}(${year - data[i].birthdate.substr(0, 4)})`
        } else if (data[i].birthdate.substr(4, 2) == month) {
            if (data[i].birthdate.substr(6, 2) <= date) {
                ageResult = `${year - data[i].birthdate.substr(0, 4) + 1}(${year - data[i].birthdate.substr(0, 4)})`
            } else {
                ageResult = `${year - data[i].birthdate.substr(0, 4) + 1}(${year - data[i].birthdate.substr(0, 4) - 1})`
            }
        } else {
            ageResult = `${year - data[i].birthdate.substr(0, 4) + 1}(${year - data[i].birthdate.substr(0, 4) - 1})`
        }

        const memberData4 = document.createElement('td');
        memberData4.setAttribute("class", `table-list_body-tr_td`);
        memberData4.innerText = ageResult
        memberList.appendChild(memberData4);

        const memberData6 = document.createElement('td');
        memberData6.setAttribute("class", `table-list_body-tr_td`);
        memberData6.innerText = data[i].role
        memberList.appendChild(memberData6);

        const memberData7 = document.createElement('td');
        memberData7.setAttribute("class", `table-list_body-tr_td`);
        memberData7.innerText = data[i].entering_date
        memberList.appendChild(memberData7);

        const memberData8 = document.createElement('td');
        memberData8.setAttribute("class", `table-list_body-tr_td`);
        memberData8.innerText = data[i].phone_num
        memberList.appendChild(memberData8);

        const memberData8Spare = document.createElement('td');
        memberData8Spare.setAttribute("class", `table-list_body-tr_td`);
        if(data[i].emergency !== ""){
            memberData8Spare.innerText = `${data[i].emergency.split(" ")[0]}(${data[i].emergency.split(" ")[1]})`
        }else{
            memberData8Spare.innerText = ""
        }
        memberList.appendChild(memberData8Spare);

        const memberData9 = document.createElement('td');
        memberData9.setAttribute("class", `table-list_body-tr_td`);
        memberData9.innerText = data[i].birthdate
        memberList.appendChild(memberData9);

        const memberData10 = document.createElement('td');
        memberData10.setAttribute("class", `table-list_body-tr_td`);
        memberData10.innerText = data[i].address
        memberList.appendChild(memberData10);

        const memberData11 = document.createElement('td');
        memberData11.setAttribute("class", `table-list_body-tr_td memberOpenPrint`);
        if(data[i].lisence_id !== undefined){
            memberData11.setAttribute("onclick", `openLisence("/HR/member/image/${data[i].lisence_id}", true)`);
        }
        memberData11.innerText = data[i].license
        memberList.appendChild(memberData11);

        const memberData12 = document.createElement('td');
        memberData12.setAttribute("class", `table-list_body-tr_td memberOpenPrint`);
        if(data[i].lisence_id !== undefined){
            memberData12.setAttribute("onclick", `openLisence("/HR/member/image/${data[i].bus_license_id}", false)`);
        }
        memberData12.innerText = data[i].bus_license
        memberList.appendChild(memberData12);
    };

    pagenation(data)
    thisPage(pageParms)
}

// 페이지네이션 표시
function pagenation(data) {

    let parms = new URLSearchParams(location.search)
    let pagenationCount = Math.ceil(data.length / 10)

    for (i = 0; i < pagenationCount; i++) {
        const pageNumber = document.createElement('span');
        pageNumber.innerText = i + 1
        pagenationBox.appendChild(pageNumber);
    };

    const pagenationNumber = pagenationBox.querySelectorAll("span")

    if (parms.has("page")) {

        let pageNationStep = Math.ceil(parseInt(parms.get("page")) / 5)

        for (i = 0; i < pagenationNumber.length; i++) {
            if ((pageNationStep - 1) * 5 > i || (pageNationStep * 5) - 1 < i) {
                pagenationNumber[i].style.display = "none"
            }
        };
    } else {
        for (i = 5; i < pagenationNumber.length; i++) {
            pagenationNumber[i].style.display = "none"
        }
    }

}


// 현재 페이지 표시
function thisPage(pageParms) {

    let parms = new URLSearchParams(location.search)

    let getPage = ""

    if (parms.has("page")) {
        getPage = pageParms.get("page")
    } else {
        getPage = 1
    }

    for (i = 0; i < pagenationBox.children.length; i++) {
        if (pagenationBox.children[i].innerText == getPage) {
            return pagenationBox.children[i].classList.add("thisPage")
        }
    };
}


// 숫자 이동
pagenationBox.addEventListener("mouseover", changePage)

function changePage() {

    let parms = new URLSearchParams(location.search)

    const pageNumber = this.querySelectorAll("span")

    for (i = 0; i < pageNumber.length; i++) {
        pageNumber[i].addEventListener("click", changePage)
    };

    function changePage() {
        if (parms.has("age")) {
            if (!parms.has("filter")) {
                location.href = `/HR/member?age=true&page=${this.innerText}`
            } else if (parms.get("filter") == "down") {
                location.href = `/HR/member?filter=down&age=true&page=${this.innerText}`
            } else if (parms.get("filter") == "up") {
                location.href = `/HR/member?filter=up&age=true&page=${this.innerText}`
            }
        } else {
            if (!parms.has("filter")) {
                location.href = `/HR/member?page=${this.innerText}`
            } else if (parms.get("filter") == "down") {
                location.href = `/HR/member?filter=down&page=${this.innerText}`
            } else if (parms.get("filter") == "up") {
                location.href = `/HR/member?filter=up&page=${this.innerText}`
            }
        }
    }
}


// 이전 버튼
prevBtn.addEventListener("click", prevPage)

function prevPage() {
    let parms = new URLSearchParams(location.search)
    if (parms.get("page") >= 2) {
        if (parms.has("age")) {
            if (!parms.has("filter")) {
                location.href = `/HR/member?age=true&page=${parseInt(parms.get("page")) - 1}`
            } else if (parms.get("filter") == "down") {
                location.href = `/HR/member?filter=down&age=true&page=${parseInt(parms.get("page")) - 1}`
            } else if (parms.get("filter") == "up") {
                location.href = `/HR/member?filter=up&age=true&page=${parseInt(parms.get("page")) - 1}`
            }
        } else {
            if (!parms.has("filter")) {
                location.href = `/HR/member?page=${parseInt(parms.get("page")) - 1}`
            } else if (parms.get("filter") == "down") {
                location.href = `/HR/member?filter=down&page=${parseInt(parms.get("page")) - 1}`
            } else if (parms.get("filter") == "up") {
                location.href = `/HR/member?filter=up&page=${parseInt(parms.get("page")) - 1}`
            }
        }
    }
}


// 다음 버튼
nextBtn.addEventListener("click", nextPage)

function nextPage() {
    let parms = new URLSearchParams(location.search)
    makeAgeData()
    if (parms.has("age")) {
        if (parms.get("page") < Math.floor(data.length / 10) && parms.has("page")) {
            if (!parms.has("filter")) {
                location.href = `/HR/member?age=true&page=${parseInt(parms.get("page")) + 1}`
            } else if (parms.get("filter") == "down") {
                location.href = `/HR/member?filter=down&age=true&page=${parseInt(parms.get("page")) + 1}`
            } else if (parms.get("filter") == "up") {
                location.href = `/HR/member?filter=up&age=true&page=${parseInt(parms.get("page")) + 1}`
            }
        } else if (parms.get("page") == 1 || !parms.has("page")) {
            if (!parms.has("filter")) {
                location.href = `/HR/member?age=true&page=2`
            } else if (parms.get("filter") == "down") {
                location.href = `/HR/member?filter=down&age=true&page=2`
            } else if (parms.get("filter") == "up") {
                location.href = `/HR/member?filter=up&age=true&page=2`
            }
        }
    } else {
        if (parms.get("page") < Math.floor(regDatas.length / 10) && parms.has("page")) {
            if (!parms.has("filter")) {
                location.href = `/HR/member?page=${parseInt(parms.get("page")) + 1}`
            } else if (parms.get("filter") == "down") {
                location.href = `/HR/member?filter=down&page=${parseInt(parms.get("page")) + 1}`
            } else if (parms.get("filter") == "up") {
                location.href = `/HR/member?filter=up&page=${parseInt(parms.get("page")) + 1}`
            }
        } else if (parms.get("page") == 1 || !parms.has("page")) {
            if (!parms.has("filter")) {
                location.href = `/HR/member?page=2`
            } else if (parms.get("filter") == "down") {
                location.href = `/HR/member?filter=down&page=2`
            } else if (parms.get("filter") == "up") {
                location.href = `/HR/member?filter=up&page=2`
            }
        }
    }
}


// 65세 필터
ageCheckbox.addEventListener("change", ageFilter)

function ageFilter() {
    let parms = new URLSearchParams(location.search)
    if (ageCheckbox.checked) {
        if (!parms.has("filter")) {
            window.location = `/HR/member?age=true`
        } else if (parms.get("filter") == "down") {
            window.location = `/HR/member?filter=down&age=true`
        } else if (parms.get("filter") == "up") {
            window.location = `/HR/member?filter=up&age=true`
        }
    } else {
        if (!parms.has("filter")) {
            window.location = `/HR/member`
        } else if (parms.get("filter") == "down") {
            window.location = `/HR/member?filter=down`
        } else if (parms.get("filter") == "up") {
            window.location = `/HR/member?filter=up`
        }
    }
}

function makeAgeData() {
    let ageData = []
    for (i = 0; i < regDatas.length; i++) {

        let now = new Date();
        let year = now.getFullYear();
        var month = now.getMonth() + 1;
        var date = now.getDate();
        let ageResult = ""

        if (regDatas[i].birthdate.substr(4, 2) < month) {
            ageResult = `${year - regDatas[i].birthdate.substr(0, 4)}`
        } else if (regDatas[i].birthdate.substr(4, 2) == month) {
            if (regDatas[i].birthdate.substr(6, 2) <= date) {
                ageResult = `${year - regDatas[i].birthdate.substr(0, 4)}`
            } else {
                ageResult = `${year - regDatas[i].birthdate.substr(0, 4) - 1}`
            }
        } else {
            ageResult = `${year - regDatas[i].birthdate.substr(0, 4) - 1}`
        }

        if (ageResult >= 65) {
            ageData.push(regDatas[i])
        }
    };

    data = ageData
}

filterHeader.addEventListener("click", upDownFilter)

function upDownFilter() {

    let parms = new URLSearchParams(location.search)
    if (!parms.has("filter")) {
        if (parms.has("age")) {
            window.location = `/HR/member?filter=up&age=true`
        } else {
            window.location = `/HR/member?filter=up`
        }
    } else {
        if (parms.get("filter") == "up") {
            if (parms.has("age")) {
                window.location = `/HR/member?filter=down&age=true`
            } else {
                window.location = `/HR/member?filter=down`
            }
        } else if (parms.get("filter") == "down") {
            if (parms.has("age")) {
                window.location = `/HR/member?filter=up&age=true`
            } else {
                window.location = `/HR/member?filter=up`
            }
        }
    }
}

function makeSortUpData(targetData) {
    let datatArry = []
    for (i = 0; i < targetData.length; i++) {
        let sortObject = {
            name: `${targetData[i].name}`,
            role: `${targetData[i].role}`
        }
        datatArry.push(sortObject)
    };
    let sortArry = datatArry.sort((a, b) => {
        if (a.role > b.role) return 1;
        if (a.role < b.role) return -1;
        return 0;
    })

    let resultArry = []
    for (i = 0; i < sortArry.length; i++) {
        for (j = 0; j < targetData.length; j++) {
            if (sortArry[i].name == targetData[j].name) {
                resultArry.push(targetData[j])
            }
        }
    };

    filterHeaderArrow.style.borderTop = "1rem solid white"
    filterHeaderArrow.style.borderBottom = "1rem solid transparent"
    filterHeaderArrow.style.marginTop = "1rem"
    filterHeaderArrow.style.marginBottom = "0"
    data = resultArry
}

function makeSortDownData(targetData) {
    let datatArry = []
    for (i = 0; i < targetData.length; i++) {
        let sortObject = {
            name: `${targetData[i].name}`,
            role: `${targetData[i].role}`
        }
        datatArry.push(sortObject)
    };
    let sortArry = datatArry.sort((a, b) => {
        if (a.role < b.role) return 1;
        if (a.role > b.role) return -1;
        return 0;
    })

    let resultArry = []
    for (i = 0; i < sortArry.length; i++) {
        for (j = 0; j < targetData.length; j++) {
            if (sortArry[i].name == targetData[j].name) {
                resultArry.push(targetData[j])
            }
        }
    };

    filterHeaderArrow.style.borderBottom = "1rem solid white"
    filterHeaderArrow.style.borderTop = "1rem solid transparent"
    filterHeaderArrow.style.marginBottom = "1rem"
    filterHeaderArrow.style.marginTop = "0"
    data = resultArry
}