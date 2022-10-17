const school = document.querySelectorAll(".school")

for (i = 0; i < school.length; i++) {
    school[i].addEventListener("input", schoolNameLink)
}

window.onload = function () {
    schoolNameLinkOnload();
    window.print();
    
}

function schoolNameLink() {
    if (this.value.length < 9) {
        for (i = 0; i < school.length; i++) {
            school[i].style.top = "28.2%"
            school[i].style.height = "1.5rem"
        }
    } else {
        for (i = 0; i < school.length; i++) {
            school[i].style.top = "27.3%"
            school[i].style.height = "2.6rem"
        }
    }
    for (i = 0; i < school.length; i++) {
        school[i].value = school[0].value
    }
}

function schoolNameLinkOnload() {
    for (i = 0; i < school.length; i++) {
        if (school[i].value.length < 9) {
            school[i].style.top = "28.2%"
            school[i].style.height = "1.5rem"
        } else {
            school[i].style.top = "27.3%"
            school[i].style.height = "2.6rem"
        }
        school[i].value = school[0].value
    }
}