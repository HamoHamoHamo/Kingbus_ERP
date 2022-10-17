// 새로고침 화면 상단이동
window.addEventListener('beforeunload', (event) => {
    event.preventDefault();
    setTimeout(function () {
        scrollTo(0, 0)
    }, 0);
  });

