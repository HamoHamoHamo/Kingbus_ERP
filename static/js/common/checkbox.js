// MARK: CheckBox

// variable

const selectAllCheckBox = document.querySelector(".checkAll");
const selectCheckBox = document.querySelectorAll(".check");

// function
const selectAll = (selectAll) => {

    selectCheckBox.forEach((checkbox) => {
        checkbox.checked = selectAll.checked;
    })
}

// eventListener
const addEventSelectAllCheck = () => {
    selectAllCheckBox.addEventListener("click", () => {
        selectAll(selectAllCheckBox);
    });
}

export { addEventSelectAllCheck };