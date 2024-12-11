const popupAreaModules = document.querySelectorAll('.popupAreaModules')
const notificationTimeBtn = document.querySelector("#notificationTimeBtn")
const notificationTimeEditBtn = document.querySelector(".notificationTimeEditBtn")

notificationTimeBtn.addEventListener("click", () => {
    popupAreaModules[4].style.display = "block"

})

notificationTimeEditBtn.addEventListener('click', () => {
    const prepare_time1 = document.querySelector('.prepare_time1')
    const prepare_time2 = document.querySelector('.prepare_time2')
    const boarding_time1 = document.querySelector('.boarding_time1')
    const boarding_time2 = document.querySelector('.boarding_time2')
    const first_stop_time1 = document.querySelector('.first_stop_time1')
    const first_stop_time2 = document.querySelector('.first_stop_time2')

    const prepare_time1Hidden = document.querySelector('input[name="prepare_time1"]')
    const prepare_time2Hidden = document.querySelector('input[name="prepare_time2"]')
    const boarding_time1Hidden = document.querySelector('input[name="boarding_time1"]')
    const boarding_time2Hidden = document.querySelector('input[name="boarding_time2"]')
    const first_stop_time1Hidden = document.querySelector('input[name="first_stop_time1"]')
    const first_stop_time2Hidden = document.querySelector('input[name="first_stop_time2"]')
    
    if (
        prepare_time1.value == "" ||
        prepare_time2.value == "" ||
        boarding_time1.value == "" ||
        boarding_time2.value == "" ||
        first_stop_time1.value == "" ||
        first_stop_time2.value == ""
    ) {
        return alert("입력하지 않은 필수 입력사항이 있습니다.")   
    } else if (
        isNaN(prepare_time1.value) ||
        isNaN(prepare_time2.value) ||
        isNaN(boarding_time1.value) ||
        isNaN(boarding_time2.value) ||
        isNaN(first_stop_time1.value) ||
        isNaN(first_stop_time2.value)
    ) {
        return alert("숫자만 입력해 주세요.")
    }

    
    
    prepare_time1Hidden.value = prepare_time1.value
    prepare_time2Hidden.value = prepare_time2.value
    boarding_time1Hidden.value = boarding_time1.value
    boarding_time2Hidden.value = boarding_time2.value
    first_stop_time1Hidden.value = first_stop_time1.value
    first_stop_time2Hidden.value = first_stop_time2.value
    popupAreaModules[4].style.display = "none"

})
