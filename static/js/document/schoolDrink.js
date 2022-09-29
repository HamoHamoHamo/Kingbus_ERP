const schoolName = document.querySelector(".schoolName")
const schoolNameLast = document.querySelector(".sent input")

schoolName.addEventListener("input", linkSchoolName)

function linkSchoolName(){
    schoolNameLast.value = `${schoolName.value}장  귀하`
}