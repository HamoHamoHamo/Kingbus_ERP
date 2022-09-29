const departure = document.querySelectorAll(".departure")
const arrival = document.querySelectorAll(".arrival")

window.onload = function(){
    departure[0].innerText = departure[0].innerText.split("<")[0]
    arrival[0].innerText = arrival[0].innerText.split("<")[0]
    departure[1].innerText = departure[1].innerText.split("<")[0]
    arrival[1].innerText = arrival[1].innerText.split("<")[0]
}