function printDiv(divId) {
    // 프린트할 내용 가져오기
    var printContents = document.getElementById(divId).innerHTML;
    // 현재 페이지의 원래 내용 저장
    var originalContents = document.body.innerHTML;

    // 페이지의 내용을 프린트할 내용으로 교체
    document.body.innerHTML = "<head><title>Print</title></head><body>" + printContents + "</body>";

    // 프린트 실행
    window.print();

    // 원래 내용 복구
    document.body.innerHTML = originalContents;

    // JavaScript 기능 다시 활성화
    window.location.reload(); // 이 코드는 페이지를 새로고침하여 JavaScript를 다시 실행합니다.
}
