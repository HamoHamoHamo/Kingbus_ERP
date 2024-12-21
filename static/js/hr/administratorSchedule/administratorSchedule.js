document.querySelectorAll(".progressBtnJs").forEach(button => {
    button.addEventListener("click", () => {
        const action = button.textContent.trim();
        const isConfirmed = confirm(`되돌리기가 불가능합니다. ${action}하시겠습니까?`);
    });
});