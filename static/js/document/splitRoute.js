const departure = document.querySelector(".departure")
const arrival = document.querySelector(".arrival")

window.onload = function (){
    departure.innerText = departure.innerText.split("@")[0]
    arrival.innerText = arrival.innerText.split("@")[0]

    departure.innerText = departure.innerText.slice(departure.innerText.lastIndexOf('>') + 1)
    arrival.innerText = arrival.innerText.slice(arrival.innerText.lastIndexOf('>') + 1)

    window.print()
}