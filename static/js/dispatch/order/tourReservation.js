const tourReservationBtn = document.querySelector(".tourReservationBtn")
const tourReservationCloseBtn = document.querySelector(".tourReservationCloseBtn")
const datetimeLocal = document.querySelectorAll(".datetimeLocal")
const selectType = document.querySelectorAll(".selectType")


tourReservationBtn.addEventListener("click", openTourReservationPopup)

function openTourReservationPopup() {
    popupAreaModules[6].style.display = "block"
}

popupBgModules[6].addEventListener("click", closeTourReservationPopup)
SidemenuUseClose.addEventListener("click", closeTourReservationPopup)
tourReservationCloseBtn.addEventListener("click", closeTourReservationPopup)

function closeTourReservationPopup() {
    popupAreaModules[6].style.display = "none"
}

Array.from(selectType).forEach(item => {
    item.addEventListener("change", setReservationCustomerId)
})

Array.from(datetimeLocal).forEach(item => {
    item.addEventListener("change", setReservationCustomerId)
})

function setReservationCustomerId(e) {
    console.log(e.target.parentNode.parentNode)
}