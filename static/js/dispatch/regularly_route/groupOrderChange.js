const groupListItems = document.querySelectorAll(".groupListItem")
const groupFixe = document.querySelectorAll(".groupFixe")
const groupListBodys = document.querySelector(".groupListBody")


window.onload = function () {
    for (i = 0; i < groupListItems.length; i++) {
        if (groupListItems[i].classList.contains("fixedGroup")) {
            groupListItems[i].children.children[2].children[0].children[0].style.fill = "#444"
        }
    }
}



// 그룹순서변경
groupListItems.forEach(groupListItem => {
    groupListItem.addEventListener("dragstart", () => {
        groupListItem.classList.add("dragging");
    });

    groupListItem.addEventListener("dragend", () => {
        groupListItem.classList.remove("dragging");
        postGroupId()
    });
});


groupListBodys.addEventListener("dragover", e => {
    e.preventDefault();
    const afterElement = getDragAfterElement(groupListBodys, e.clientY);
    const groupListItem = document.querySelector(".dragging");
    if (afterElement === undefined) {
        groupListBodys.appendChild(groupListItem);
    } else {
        groupListBodys.insertBefore(groupListItem, afterElement);
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
    postGroupId()
}





// fetch

let orderArr = []

async function postGroupId() {
    const groupListItem = document.querySelectorAll(".groupListItem")
    for (i = 0; i < groupListItem.length; i++) {
        orderArr.push(groupListItem[i].classList[1])
    }
    const response = await fetch(url, {
        method: "post",
        body: `${orderArr}`
    })
        .then((response) => response.json())
        .then((result) => {
            console.log('성공:', result);
        })
        .catch((error) => {
            alert('위치변경에 실패했습니다.', error)
        });
}

// fetch or ajax로 클릭할때마다 전송(hidden에 그룹 아이디)
// fixe 데이터를 받으면 html 그릴때 groupListItem fixedGroup클래스 부여
//groupListItem 클래스가 있으면 path에 fill 변경