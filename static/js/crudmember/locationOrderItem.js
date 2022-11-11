function locationOrder(){
    let locationDate = `${dateTitle.innerText.substr(0,4)}-${dateTitle.innerText.substr(6,2)}`
    let lastDay = new Date(locationDate.substr(0,4), locationDate.substr(5,2), 0).getDate();
    location.href = `dispatch/order?search=${this.children[0].innerText}&type=customer&date1=${locationDate}-01&date2=${locationDate}-${lastDay}`
}