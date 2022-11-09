const groupListItems = document.querySelectorAll(".groupListItem")
const groupListBodys = document.querySelector(".groupListBody")
const groupLock = document.querySelector(".groupLock")
const lockClose = document.querySelector(".lockClose")
const lockOpen = document.querySelector(".lockOpen")


let orderArr = []
let fixeCounter = 0
let lockState = false

groupLock.addEventListener("click", lockBtn)

function lockBtn() {
    if (!lockState && confirm("그룹목록순서를 수정하시겠습니까?")) {
        lockState = true
        lockClose.style.display = "none"
        lockOpen.style.display = "block"
    } else {
        lockState = false
        lockClose.style.display = "block"
        lockOpen.style.display = "none"
    }
}


// 그룹순서변경
groupListItems.forEach(groupListItem => {
    groupListItem.addEventListener("dragstart", (e) => {
        if (lockState) {
            groupListItem.classList.add("dragging");
        }
    });

    groupListItem.addEventListener("dragend", () => {
        if (lockState) {
            groupListItem.classList.remove("dragging");
            makeData()
        }
    });
});


groupListBodys.addEventListener("dragover", e => {
    e.preventDefault();
    const afterElement = getDragAfterElement(groupListBodys, e.clientY);
    const groupListItem = document.querySelector(".dragging");
    if (groupListItem !== null) {
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