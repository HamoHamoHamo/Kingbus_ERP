const calenderDataBox = document.querySelectorAll(".calender_date_box")

for (i = 0; i < calenderDataBox.length; i++) {
    calenderDataBox[i].addEventListener("click", selectingDataBox)
};

function selectingDataBox() {
    if (this.classList.contains("selecting")) {
        for (i = 0; i < calenderDataBox.length; i++) {
            calenderDataBox[i].classList.remove("selecting")
        };
    } else {
        for (i = 0; i < calenderDataBox.length; i++) {
            calenderDataBox[i].classList.remove("selecting")
        };
        this.classList.add("selecting")

    }
}
