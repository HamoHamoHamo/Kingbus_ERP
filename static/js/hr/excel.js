const uploadExcelBtn = document.querySelector("#uploadExcelBtn")
const downloadExcelBtn = document.querySelector("#downloadExcelBtn")

downloadExcelBtn.addEventListener('click', downloadExcel);

function downloadExcel() {
    if (confirm('직원 목록을 다운로드 하시겠습니까?')) {
        window.location.href=excelDownloadUrl;
    }
}

// 엑셀 업로드 팝업 열기
uploadExcelBtn.addEventListener("click", () => {
  popupAreaModules[1].style.display = 'block'
})