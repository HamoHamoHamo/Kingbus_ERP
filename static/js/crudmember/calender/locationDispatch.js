const scheduleRegularlyCell = document.querySelectorAll(".regularly_cnt_cell")
const scheduleOrderCell = document.querySelectorAll(".order_cnt_cell")

let thisYear = calenderDate.innerText.substr(0,4)
let thisMonth = calenderDate.innerText.substr(6,2)

for (i = 0; i < scheduleRegularlyCell.length-1; i++){
    scheduleRegularlyCell[i].addEventListener("click", locationRegularlyDispatch)
    scheduleOrderCell[i].addEventListener("click", locationOrderDispatch)
};

function locationRegularlyDispatch(e){
    e.stopPropagation()
    let thisDate = this.parentNode.parentNode.parentNode.children[0].children[0].innerText
    if(thisDate <= 9){
        thisDate = `0${thisDate}`
    }
    location.href = `dispatch/regularly?date=${thisYear}-${thisMonth}-${thisDate}`
}

function locationOrderDispatch(e){
    e.stopPropagation()
    let thisDate = this.parentNode.parentNode.parentNode.children[0].children[0].innerText
    if(thisDate <= 9){
        thisDate = `0${thisDate}`
    }
    location.href = `dispatch/order?date1=${thisYear}-${thisMonth}-${thisDate}&date2=${thisYear}-${thisMonth}-${thisDate}`
}