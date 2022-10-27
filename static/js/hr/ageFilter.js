const agefilter = document.querySelector("#ageFilter")

agefilter.addEventListener("change", ageFiltering)

function ageFiltering() {
    if (agefilter.checked) {
        for (i = 0; i < age.length; i++) {
            if (age[i].innerText.split("(")[1].replace(/\)/g, "") < 65) {
                age[i].parentNode.style.display = "none"
            }
        };
    }else{
        for (i = 0; i < age.length; i++) {
            if (age[i].innerText.split("(")[1].replace(/\)/g, "") < 65) {
                age[i].parentNode.style.display = "table-row"
            }
        };
    }
}