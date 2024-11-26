const auto = document.querySelectorAll('.auto')
const autoBtn = document.querySelector('.autoBtn')

autoBtn.addEventListener('click', () => {
    autoBtn.value = autoBtn.value == '자동' ? "수동" : "자동"

    Array.from(auto).forEach(item => {
        item.style.display = autoBtn.value == "자동" ? "none" : "block"
    })
})
