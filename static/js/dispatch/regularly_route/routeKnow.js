const routeListBodyTr = document.querySelectorAll(".RouteListBodyTr")
const RouteListHeadScroll = document.querySelector(".RouteListHeadScroll")
const RouteListScroll = document.querySelector(".RouteListScroll")
const popup = document.querySelector(".popupAreaModules");
const popupBg = document.querySelector("#detailMapPopupBg")
const popupCloseBtn = document.querySelector("#detailPopupCloseBtn")
const orderRoute = document.querySelectorAll(".orderRoute")
const routeId = document.querySelector("#routeId")
const popupTbody = document.querySelector("#detailMapTable")
let popupCheckbox = document.querySelectorAll("#detailMapTable input[type=checkbox]")
let popupAllCheckbox = document.querySelector(".detailMapPopupHeader input[type=checkbox]")
const popupSaveBtn = document.querySelector(".popupSaveBtn")
const deleteBtn = document.querySelector("#deleteBtn")
const deleteForm = document.querySelector("#deleteForm")

let noPopup = 0;

function openKnowListPopup() {
    if (noPopup == 0) {
        popup.style.display = 'block';
        routeId.value = this.classList[1];

        let knowData = knows[this.classList[1]];
        for (i=0; i<knowData.length; i++) {
            let tr = document.importNode(document.querySelector("#popupTr").content, true).firstElementChild;
            tr.className = knowData[i]['driver_id__id'];
            console.log("TST", tr.children[0]);
            tr.children[0].children[0].value = knowData[i]['id'];
            tr.children[1].innerText = i + 1;
            tr.children[2].innerText = knowData[i]['driver_id__name']
            tr.children[3].innerText = knowData[i]['driver_id__role']
            popupTbody.append(tr);
        }
        popupCheckbox = document.querySelectorAll("#detailMapTable input[type=checkbox]")
        for (i = 0; i < popupCheckbox.length; i++){
            popupCheckbox[i].addEventListener('change', popupDeletecheck)
        };
    }
    noPopup = 0;
}

function closeKnowListPopup() {
    popup.style.display = "none";
    trs = document.querySelectorAll('#detailMapTable tr')
    for (i = 0; i < trs.length; i++){
        trs[i].remove();
    };
    
}

function loadTargetRoute() {
    let parms = new URLSearchParams(location.search)
    noPopup = 1;
    if (parms.has("search")) {
        location.href = `${regularlyRouteUrl}?id=${this.parentNode.classList[1]}&group=${this.parentNode.classList[2]}&use={{search_use}}&search=${parms.get("search")}&height=${this.parentNode.parentNode.parentNode.parentNode.scrollTop}`
    } else {
        location.href = `${regularlyRouteUrl}?id=${this.parentNode.classList[1]}&group=${this.parentNode.classList[2]}&use={{search_use}}&height=${this.parentNode.parentNode.parentNode.parentNode.scrollTop}`
    }
}

// 콤마 추가
function addComma() {
    for (i = 0; i < routeListBodyTr.length; i++) {
        routeListBodyTr[i].children[8].innerText = routeListBodyTr[i].children[8].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        routeListBodyTr[i].children[9].innerText = routeListBodyTr[i].children[9].innerText.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
    }
}

RouteListScroll.addEventListener("scroll", scrollLink)

function scrollLink() {
    RouteListHeadScroll.scrollLeft = RouteListScroll.scrollLeft
}

function popupDeletecheck(e){
    e.stopPropagation()
    console.log("TEST")
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

function popupAllDeleteCheck(){
    let popupCheckbox = document.querySelectorAll("#detailMapTable input[type=checkbox]")

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


window.onload = function () {
    addComma();

    popupBg.addEventListener('click', closeKnowListPopup)
    popupCloseBtn.addEventListener('click', closeKnowListPopup)

    for (i = 0; i < orderRoute.length; i++) {
        orderRoute[i].addEventListener("click", loadTargetRoute)
    };
    
    for (let i = 0; i < routeListBodyTr.length; i++) {
        routeListBodyTr[i].addEventListener('click', openKnowListPopup)
    }

    let parms = new URLSearchParams(location.search)

    if (parms.has("group")) {
        const groupListItem = document.querySelectorAll(".groupListItem")
        for (i = 0; i < groupListItem.length; i++) {
            if (groupListItem[i].classList[1] == parms.get("group")) {
                groupListItem[i].style.backgroundColor = "#CDCDCE"
            }
        };
    }

    popupAllCheckbox.addEventListener("change", popupAllDeleteCheck)

    deleteBtn.addEventListener('click', () => {
        if (confirm('정말로 삭제하시겠습니까?')) {
            deleteForm.submit();
        }
    })
}