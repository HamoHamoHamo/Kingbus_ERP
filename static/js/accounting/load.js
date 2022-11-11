const depositLoadBtn = document.querySelector(".depositLoadBtn")
const loadingBg = document.querySelector(".loadingBg")

depositLoadBtn.addEventListener("click", loadDeposit)

function loadDeposit() {
    loadingBg.style.display = "flex"
    $.ajax({
        url: "/accounting/deposit/data",
        method: "POST",
        datatype: 'json',
        success: function (result) {
            if (result) {
                loadingBg.style.display = "none"
                alert(`${result.count}개의 입금내역을 불러왔습니다.`)
            } else { 
                loadingBg.style.display = "none"
                alert("입금내역을 불러오지 못했습니다.")
            }
        },
        error: function (request, error) {
            console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
        },
    });
}