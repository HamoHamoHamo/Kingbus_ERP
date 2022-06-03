const profile = document.querySelector(".profile")
const profileBox = document.querySelector(".profileBox")
const Sidemenu = document.querySelector(".Sidemenu")
const mainContentsCentainer = document.querySelector(".mainContentsCentainer")


profile.addEventListener("click", openProfile)
Sidemenu.addEventListener("click", closeProfile1)
mainContentsCentainer.addEventListener("click", closeProfile2)


let profileCount = 0;

function openProfile() {
  if (profileCount == 0) {
    profileBox.style.display = "flex"
    profileCount = 1;
  } else{
    profileBox.style.display = "none"
    profileCount = 0;
  }
}

function closeProfile1() {
  profileBox.style.display = "none"
}

function closeProfile2() {
  profileBox.style.display = "none"
}