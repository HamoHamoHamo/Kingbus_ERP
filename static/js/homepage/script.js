const hembugeIcon = document.querySelector('.hembugeIcon')
const dropDownMenu = document.querySelector('.dropDownMenu')
const hembugeLineTop = document.querySelector('.hembugeIcon div:nth-child(1)')
const hembugeLineMiddle = document.querySelector('.hembugeIcon div:nth-child(2)')
const hembugeLineBottom = document.querySelector('.hembugeIcon div:nth-child(3)')

let switching = 0;

hembugeIcon.addEventListener('click', openNav)

function openNav() {
  if (switching == 0) {
    dropDownMenu.style.height = '40vh';
    hembugeLineMiddle.style.opacity = '0';
    hembugeLineTop.style.transform = 'rotate(36deg) translate(0, 0.95rem)'
    hembugeLineBottom.style.transform = 'rotate(-36deg) translate(0, -0.95rem)'
    switching = 1;
  } else {
    dropDownMenu.style.height = '0';
    hembugeLineMiddle.style.opacity = '1';
    hembugeLineTop.style.transform = 'rotate(0) translate(0, 0)'
    hembugeLineBottom.style.transform = 'rotate(0) translate(0, 0)'
    switching = 0;

  }
}