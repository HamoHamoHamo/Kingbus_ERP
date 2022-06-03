const deleteBtn = document.querySelector(".deleteForm")

deleteBtn.addEventListener("submit", deletAlert)

function deletAlert(event) {
  event.preventDefault();
  if (confirm('정말 삭제하시겠습니까?')) {
    deleteBtn.submit()
  } else {
    return false;
  }
}