const groupListItems = document.querySelectorAll(".groupListItem")
const groupFixe = document.querySelectorAll(".groupFixe")
const groupListBodys = document.querySelector(".groupListBody")


function visivleFix() {
    for (i = 0; i < groupListItems.length; i++) {
        if (groupListItems[i].classList.contains("fixedGroup")) {
            groupListItems[i].children[2].children[0].children[0].style.fill = "#444"
        }
        if (window.location.search !== "") {
            if (window.location.search.split("group=")[1].split("&")[0] == groupListItems[i].classList[1]) {
                groupListItems[i].style.backgroundColor = "#CDCDCE"
            }
        }
    }
}


let orderArr = []
let fixeCounter = 0



// 그룹순서변경
groupListItems.forEach(groupListItem => {
    groupListItem.addEventListener("dragstart", (e) => {
        if(!e.target.classList.contains("fixedGroup")){
            groupListItem.classList.add("dragging");
        }
    });

    groupListItem.addEventListener("dragend", () => {
        groupListItem.classList.remove("dragging");
        makeData()
    });
});


groupListBodys.addEventListener("dragover", e => {
    e.preventDefault();
    const afterElement = getDragAfterElement(groupListBodys, e.clientY);
    const groupListItem = document.querySelector(".dragging");
    if(groupListItem !== null){
        if (afterElement === undefined) {
            groupListBodys.appendChild(groupListItem);
        } else {
            groupListBodys.insertBefore(groupListItem, afterElement);
        }
    }
});

function getDragAfterElement(groupListBodys, Y) {
    const groupListItemElements = [
        ...groupListBodys.querySelectorAll(".groupListItem:not(.dragging)"),
    ];

    return groupListItemElements.reduce(
        (closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = Y - box.top - box.height / 2;
            // console.log(offset);
            if (offset < 0 && offset > closest.offset) {
                return { offset: offset, element: child };
            } else {
                return closest;
            }
        },
        { offset: Number.NEGATIVE_INFINITY },
    ).element;
}






// 그룹고정
for (i = 0; i < groupFixe.length; i++) {
    groupFixe[i].addEventListener("click", fixedGroup)
}

function fixedGroup() {

    if (this.parentNode.classList.contains("fixedGroup")) {
        let groupListItem = this.parentNode
        let afterElementAll = this.parentNode.parentNode.querySelectorAll(".groupListItem")
        let afterElement = ""
        for (i = 0; i < afterElementAll.length; i++) {
            console.log(afterElementAll[i])
            if (!afterElementAll[i].classList.contains("fixedGroup")) {
                afterElement = afterElementAll[i]
                break;
            }
        }

        groupListBodys.insertBefore(groupListItem, afterElement);

        this.children[0].children[0].style.fill = "#dededf"
        this.parentNode.classList.remove("fixedGroup")
    } else {
        let groupListItem = this.parentNode
        let afterElementAll = this.parentNode.parentNode.querySelectorAll(".groupListItem")
        let afterElement = afterElementAll[0]

        groupListBodys.insertBefore(groupListItem, afterElement);

        this.children[0].children[0].style.fill = "#444"
        this.parentNode.classList.add("fixedGroup")
    }
    makeData()
}


// makeData

function makeData() {
    let orderArr = []
    let fixeCounter = 0
    const groupListItem = document.querySelectorAll(".groupListItem")
    for (i = 0; i < groupListItem.length; i++) {
        orderArr.push(groupListItem[i].classList[1])
    }
    for (i = 0; i < groupListItem.length; i++) {
        if (groupListItem[i].classList.contains("fixedGroup")) {
            fixeCounter = fixeCounter + 1
        }
    }
    data = {
        order: orderArr,
        fix: fixeCounter
    }
    postGroupId(url = "group/fix", data)
}



// fetch
async function postGroupId(url, data) {
    var headers = new Headers();
    var csrftoken = getCookie('csrftoken');
    headers.append('X-CSRFToken', csrftoken);
    headers.append('Accept', 'application/json, text/plain, */*');
    headers.append('Content-Type', 'application/x-www-form-urlencoded, application/json');

    const response = await fetch(url, {
        method: "post",
        credentials: "include",
        headers: headers,
        body: JSON.stringify(data)
    })
        .then((response) => response.json())
        .then((result) => {
            console.log('성공:', result);
        })
        .catch((error) => {
            alert('위치변경에 실패했습니다.', error)
            console.log(data)
        });
}