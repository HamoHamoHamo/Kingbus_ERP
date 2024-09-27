// 팝업 배경 클릭 시 팝업 닫기
document.querySelectorAll('.popupBgModules').forEach((popupBg) => {
    popupBg.addEventListener('click', function() {
        // 팝업 닫기
        this.closest('.popupAreaModules').style.display = 'none';
    });
});

// 팝업 내부 클릭 시 이벤트가 버블링되지 않도록 처리
document.querySelectorAll('.popupContainer').forEach((popupContent) => {
    popupContent.addEventListener('click', function(event) {
        event.stopPropagation();  // 이벤트가 부모로 전파되지 않도록 함
    });
});