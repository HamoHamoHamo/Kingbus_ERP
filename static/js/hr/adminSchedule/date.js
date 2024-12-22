// DOM 요소 가져오기
const prevButton = document.querySelector("#prev");
const nextButton = document.querySelector("#next");
const datePicker = document.querySelector("#datePicker");
const addTodoButton = document.querySelector("#addTodoButton"); // 할 일 추가 버튼

// 현재 URL에서 date 파라미터를 가져오거나 오늘 날짜로 초기화
const urlParams = new URLSearchParams(window.location.search);
let currentDate = urlParams.get("date") ? new Date(urlParams.get("date")) : new Date();
initializeDatePicker();
updateAddTodoLink(); // 초기화 시 "할 일 추가" 버튼 링크 설정

// 이전 날짜로 이동
prevButton.addEventListener("click", (e) => {
    e.preventDefault(); // 기본 동작 방지
    changeDate(-1); // 하루 전으로 이동
});

// 다음 날짜로 이동
nextButton.addEventListener("click", (e) => {
    e.preventDefault(); // 기본 동작 방지
    changeDate(1); // 하루 후로 이동
});

// 달력에서 날짜 선택 시 URL 업데이트
datePicker.addEventListener("change", (e) => {
    const selectedDate = new Date(e.target.value);
    currentDate = selectedDate; // 선택한 날짜로 갱신
    updateUrlWithDate(formatDate(selectedDate)); // URL 업데이트
    updateAddTodoLink(); // "할 일 추가" 버튼 링크 업데이트
});

// 날짜 초기화 함수
function initializeDatePicker() {
    datePicker.value = formatDate(currentDate); // 현재 날짜를 달력에 설정
}

// 날짜 변경 함수
function changeDate(offset) {
    currentDate.setDate(currentDate.getDate() + offset); // 날짜 조정
    const formattedDate = formatDate(currentDate);
    datePicker.value = formattedDate; // 달력 업데이트
    updateUrlWithDate(formattedDate); // URL 변경하여 GET 요청
    updateAddTodoLink(); // "할 일 추가" 버튼 링크 업데이트
}

// 날짜 형식 변환 함수 (YYYY-MM-DD)
function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0"); // 월은 0부터 시작
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
}

function updateUrlWithDate(date) {
    if (!date) {
        console.error("date 값이 유효하지 않습니다:", date);
        return;
    }

    try {
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set("date", date);

        // 메시지 생성
        const logMessage = `업데이트된 URL: ${currentUrl.toString()}`;
        console.log(logMessage);

        // 디버깅 메시지를 localStorage에 저장
        localStorage.setItem("debugLog", logMessage);

        // URL 변경 및 새로고침
        window.location.href = currentUrl.toString();
    } catch (error) {
        console.error("URL 업데이트 중 오류 발생:", error);

        // 오류 메시지도 저장
        localStorage.setItem("debugLog", `오류 발생: ${error.message}`);
    }
}

// 새로고침 후 저장된 메시지를 출력
window.addEventListener("load", () => {
    const savedLog = localStorage.getItem("debugLog");
    if (savedLog) {
        console.log("디버깅 메시지:", savedLog);
        localStorage.removeItem("debugLog"); // 출력 후 삭제
    }
});

// "할 일 추가" 버튼 링크 업데이트 함수
function updateAddTodoLink() {
    const baseUrl = "http://35.232.200.138/assignment/temporary"; // 루트 URL
    const date = formatDate(currentDate); // 현재 선택된 날짜
    console.log("현재날짜:", date);
    const newUrl = `${baseUrl}?date1=${date}&date2=${date}`;
    console.log("새로운 '할 일 추가' URL:", newUrl); // 생성된 URL 출력
    addTodoButton.setAttribute("href", newUrl); // "할 일 추가" 버튼의 href 설정
}
