const departure = document.querySelector(".departure")
const arrival = document.querySelector(".arrival")

window.onload = function(){
    departure.innerText = departure.innerText.split("<")[0]
    arrival.innerText = arrival.innerText.split("<")[0]
}