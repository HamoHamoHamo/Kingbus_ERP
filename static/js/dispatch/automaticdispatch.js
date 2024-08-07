function openDetails() {
  var details = document.querySelector(".orderListSub");
  var button = document.querySelector(".buttons button");
  var headerLine = document.querySelector(".headerLine");
  var isDetailsShown = headerLine.classList.contains("details-shown");

  if (details.classList.contains("hidden")) {
    details.classList.remove("hidden");
    button.textContent = "상세사항 닫기";

    if (!isDetailsShown) {
      // Add extra columns to the header
      for (let i = 1; i <= 7; i++) {
        const newTh = document.createElement("th");
        newTh.textContent = `상세${i}`;
        newTh.style.width = "150px"; // Set width for new columns
        headerLine.appendChild(newTh);
      }
      headerLine.classList.add("details-shown");

      // Add extra columns to each row
      var rows = document.querySelectorAll(".tableBodydispatch .bodyLine");
      rows.forEach((row) => {
        for (let i = 1; i <= 7; i++) {
          const newTd = document.createElement("td");
          newTd.textContent = `상세${i}`;
          newTd.style.width = "150px"; // Set width for new cells
          row.appendChild(newTd);
        }
        row.classList.add("details-shown");
      });

      // Increase table width
      document.querySelector(".tableHeaddispatch table").style.width = `${
        headerLine.children.length * 150
      }px`;
      document.querySelector(".tableBodydispatch table").style.width = `${
        headerLine.children.length * 150
      }px`;
    }
  } else {
    details.classList.add("hidden");
    button.textContent = "상세사항 열기";

    if (isDetailsShown) {
      // Remove extra columns from the header
      for (let i = 0; i < 7; i++) {
        headerLine.removeChild(headerLine.lastChild);
      }
      headerLine.classList.remove("details-shown");

      // Remove extra columns from each row
      var rows = document.querySelectorAll(".tableBodydispatch .bodyLine");
      rows.forEach((row) => {
        for (let i = 0; i < 7; i++) {
          row.removeChild(row.lastChild);
        }
        row.classList.remove("details-shown");
      });

      // Decrease table width
      document.querySelector(".tableHeaddispatch table").style.width = `${
        headerLine.children.length * 150
      }px`;
      document.querySelector(".tableBodydispatch table").style.width = `${
        headerLine.children.length * 150
      }px`;
    }
  }
}

function downloadExcel() {
  // Implement Excel download logic here
  alert("엑셀이 다운로드 되었습니다.");
}

function showPopup() {
  document.getElementById("popup").style.display = "block";
}

function closePopup() {
  document.getElementById("popup").style.display = "none";
}

function saveChanges() {
  // Implement save functionality
  alert("변경사항이 저장되었습니다.");
  closePopup();
}
