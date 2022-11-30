const crete = document.querySelector(".popup-area-box_btn")
const popupAreaModules = document.querySelectorAll(".popupAreaModules")
const popupBgModules = document.querySelectorAll(".popupBgModules")
const popupCloseBtn = document.querySelectorAll(".popupCloseBtn")
const SidemenuUseClose = document.querySelector(".Sidemenu")
const client = document.querySelectorAll(".client")
const editBusiness = document.querySelector(".editBusiness")
const editAccount = document.querySelector(".editAccount")
const editCeo = document.querySelector(".editCeo")
const editCeoPhone = document.querySelector(".editCeoPhone")
const editWorker = document.querySelector(".editWorker")
const editWorkerPhone = document.querySelector(".editWorkerPhone")
const editEmail = document.querySelector(".editEmail")
const editAddress = document.querySelector(".editAddress")
const editBlanck = document.querySelector(".editBlanck")
const accountTr = document.querySelectorAll(".accountTr")
const editAccountId = document.querySelector(".editAccountId")

crete.addEventListener("click", openCreatePopup)

function openCreatePopup(){
    popupAreaModules[0].style.display = "block"
}

popupBgModules[0].addEventListener("click", closePopup)
popupBgModules[1].addEventListener("click", closePopup)
popupCloseBtn[0].addEventListener("click", closePopup)
popupCloseBtn[1].addEventListener("click", closePopup)
SidemenuUseClose.addEventListener("click", closePopup)

function closePopup(){
    popupAreaModules[0].style.display = "none"
    popupAreaModules[1].style.display = "none"
    editBusiness.value = ""
    editAccount.value = ""
    editCeo.value = ""
    editCeoPhone.value = ""
    editWorker.value = ""
    editWorkerPhone.value = ""
    editEmail.value = ""
    editAddress.value = ""
    editBlanck.value = ""
    editAccountId.value = ""
}




for (i = 0; i < client.length; i++){
    client[i].addEventListener("click", openEditPopup)
};

function openEditPopup(e){
    e.stopPropagation()
        popupAreaModules[1].style.display = "block"
        let loadEditData = ""
        for (i = 0; i < accountTr.length; i++){
            if(accountTr[i] === this.parentNode){
                loadEditData = i
            }
        };
        editBusiness.value = dataList[loadEditData].business_num
        editAccount.value = dataList[loadEditData].name
        editCeo.value = dataList[loadEditData].representative
        editCeoPhone.value = dataList[loadEditData].phone
        editWorker.value = dataList[loadEditData].manager
        editWorkerPhone.value = dataList[loadEditData].manager_phone
        editEmail.value = dataList[loadEditData].email
        editAddress.value = dataList[loadEditData].address
        editBlanck.value = dataList[loadEditData].note
        editAccountId.value = dataList[loadEditData].id
}