const select = document.querySelectorAll(".tableSelect");
const saveBtn = document.querySelector("#saveBtn");
const form = document.querySelector(".deleteForm");


for (i=0; i<select.length; i++)
    select[i].addEventListener('change', changeSelect);

saveBtn.addEventListener('click', saveStatus);

function changeSelect()
{
    this.setAttribute('name', 'status');
    
    this.parentNode.parentNode.children[0].children[0].checked = true;
}

function saveStatus() {
    form.action = saveUrl;
    form.removeAttribute('onsubmit');
    console.log(form);
    form.submit();
}
