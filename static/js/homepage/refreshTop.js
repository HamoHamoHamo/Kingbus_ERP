// // 새로고침 화면 상단이동
// window.addEventListener('beforeunload', (event) => {
//     event.preventDefault();
//     setTimeout(function () {
//         scrollTo(0, 0)
//     }, 0);
//   });
const body = document.querySelector("body")

window.onload = function () {
    if (window.innerWidth < 768) {
        body.style.height  = "100%"
        body.style.overflow = "hidden"
        body.style.touchAction  = "none"
    }

    setTimeout(function () {
        window.scrollTo({top: 0, behavior: "smooth"})
    }, 100);
}
