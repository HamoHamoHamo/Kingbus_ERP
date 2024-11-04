const tableSelects = document.querySelectorAll(".tableSelect")
const teamSaveForm = document.querySelector(".teamSaveForm")


for (i = 0; i < tableSelects.length; i++){
    tableSelects[i].addEventListener("change", createIdInput)
};

function createIdInput() {
    if(this.parentNode.parentNode.children[7] === undefined){
        console.log("TEST", this)
        this.setAttribute("name", "team_id")
        const hidden = document.createElement("input")
        hidden.setAttribute("class", "teamSaveId")
        hidden.setAttribute("type", "hidden")
        hidden.setAttribute("name", "id")
        hidden.setAttribute("value", this.parentNode.className)
        this.parentNode.parentNode.appendChild(hidden)
    }
}

teamSaveForm.addEventListener("submit", checkNoValue)

function checkNoValue(event) {
    event.preventDefault();
    const teamSaveId = document.querySelectorAll(".teamSaveId")
    if (teamSaveId.length < 1) {
        window.alert("변경된 항목이 없습니다.")
        return
    }

    teamSaveForm.submit()
}