const sideNavControll = document.querySelectorAll(".nav1BoxMenuHaveDepth2 .sideMenuArrow");
const nav1BoxMenuHaveDepth2 = document.querySelectorAll(".nav1BoxMenuHaveDepth2");
const sideMenuNav2Box = document.querySelectorAll(".sideMenuNav2Box");
const sideMenuNav2 = document.querySelectorAll(".sideMenuNav2");
const nav1Box = document.querySelectorAll(".nav1Box");

let overlapCount = 111;
let navOpenCount = false;

for (let i = 0; i < nav1BoxMenuHaveDepth2.length; i++) {
  nav1BoxMenuHaveDepth2[i].addEventListener("click", openSideNav);
}

function openSideNav() {
  const idx = Array.from(nav1BoxMenuHaveDepth2).indexOf(this);
  for (let i = 0; i < nav1BoxMenuHaveDepth2.length; i++) {
    sideMenuNav2Box[i].style.height = "0";
    sideMenuNav2[i].style.height = "0";
    sideNavControll[i].style.transform = "rotate(0deg)";
    nav1Box[i + 1].style.backgroundColor = "#1C1A4E";
  }
  
  if (overlapCount === idx) {
    sideMenuNav2Box[idx].style.height = "0";
    sideMenuNav2[idx].style.height = "0";
    overlapCount = 111;
    navOpenCount = false;
  } else {
    switch (idx) {
      case 0:
        sideMenuNav2Box[idx].style.height = "26.6rem";
        sideMenuNav2[idx].style.height = "24.6rem";
        break;
      case 1:
        if (typeof AUTHORITY !== "undefined" && AUTHORITY === 3)
          sideMenuNav2Box[idx].style.height = "18.4rem";
        else
          sideMenuNav2Box[idx].style.height = "10.4rem";
        sideMenuNav2[idx].style.height = "8.4rem";
        break;
      case 2:
        sideMenuNav2Box[idx].style.height = "14.6rem";
        sideMenuNav2[idx].style.height = "12.6rem";
        break;
      case 3:
        sideMenuNav2Box[idx].style.height = "10.4rem";
        sideMenuNav2[idx].style.height = "8.4rem";
        break;
      case 4:
        sideMenuNav2Box[idx].style.height = "10.4rem";
        sideMenuNav2[idx].style.height = "8.4rem";
        break;
      case 5:
        sideMenuNav2Box[idx].style.height = "14.4rem";
        sideMenuNav2[idx].style.height = "12.4rem";
        break;
      case 6:
        sideMenuNav2Box[idx].style.height = "47.4rem";
        sideMenuNav2[idx].style.height = "44.4rem";
        break;
      case 7:
        sideMenuNav2Box[idx].style.height = "44.4rem";
        sideMenuNav2[idx].style.height = "42.4rem";
        break;
      case 8:
        sideMenuNav2Box[idx].style.height = "22.4rem";
        sideMenuNav2[idx].style.height = "20.4rem";
        break;
      case 9:
        sideMenuNav2Box[idx].style.height = "18.4rem";
        sideMenuNav2[idx].style.height = "16.4rem";
        break;
      case 10:
        sideMenuNav2Box[idx].style.height = "14.4rem";
        sideMenuNav2[idx].style.height = "12.4rem";
        break;
      case 11:
        sideMenuNav2Box[idx].style.height = "14.4rem";
        sideMenuNav2[idx].style.height = "12.4rem";
        break;
      case 12:
        sideMenuNav2Box[idx].style.height = "22.4rem";
        sideMenuNav2[idx].style.height = "20.4rem";
        break;
      case 13:
        sideMenuNav2Box[idx].style.height = "51.6rem";
        sideMenuNav2[idx].style.height = "49.6rem";
        break;
      case 14:
        sideMenuNav2Box[idx].style.height = "10.4rem";
        sideMenuNav2[idx].style.height = "8.4rem";
        break;
    }

    sideNavControll[idx].style.transform = "rotate(180deg)";
    this.parentNode.style.backgroundColor = "#19173B";
    overlapCount = idx;
    navOpenCount = true;
  }
}



// hover 색 변화
for (let i = 0; i < nav1Box.length; i++) {
  nav1Box[i].addEventListener('mouseover', bgThis);
  nav1Box[i].addEventListener('mouseout', bgNotThis);
}

function bgThis() {
  if (!navOpenCount) {
    this.style.backgroundColor = "#19173B";
  }
}

function bgNotThis() {
  if (!navOpenCount) {
    this.style.backgroundColor = "#1C1A4E";
  }
}
