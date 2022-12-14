const changeIdPopup = document.querySelector(".change_id_popup")
const idChangeMenu = document.querySelector(".id_change_menu")
const overlapBtn = document.querySelector(".overlap_checking_btn")
const newID = document.querySelector(".overlap_checking_input")
const essentialId = document.querySelectorAll(".id_essential")
const changeIdBtn = document.querySelector(".id_change_btn")
const idChangePw = document.querySelector(".id_change_pw")


// 팝업 열기
idChangeMenu.addEventListener("click", idChangeFtn)

function idChangeFtn(e) {
    e.stopPropagation()
    if (changeIdPopup.style.display === "block") {
        closePopup(false, "nothing")
    } else {
        closePopup(true, "id")
        changeIdPopup.style.display = "block"
    }
}



// 중복 확인
overlapBtn.addEventListener("click", idOverlapCheck)

function idOverlapCheck() {
    if (essentialId[1].value === "") {
        return alert("새 아이디를 입력해 주세요.")
    }

    $.ajax({
        url: "/member/id-check",
        data: {
            'user_id': newID.value
        },
        datatype: 'json',
        success: function (data) {
            if (data['overlap'] == "fail") {
                alert("이미 존재하는 아이디 입니다.");
                newID.focus();
                return;
            } else {
                alert("사용가능한 아이디 입니다.");
                $('.overlap_checking_input').attr("check_result", "success");
                return;
            }
        },
        error: function (request, status, error) {
            console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
        }
    });
}


changeIdBtn.addEventListener("click", changeIdFtn)

function changeIdFtn() {
    for (i = 0; i < essentialId.length; i++) {
        if (essentialId[i].value === "") {
            return alert("입력하지 않은 필수 입력사항이 있습니다.")
        }
    };

    if (newID.getAttribute("check_result") !== "success") {
        return alert("아이디 중복확인을 진행해 주세요")
    }

    $.ajax({
        url: "/member/change/id",
        method: "POST",
        data: {
            'user_id': newID.value,
            'password': idChangePw.value,
            'csrfmiddlewaretoken': csrftoken,
            'X-CSRFToken': csrftoken
        },
        datatype: 'json',
        success: function (data) {
            if (data['status'] == "fail") {
                alert("비밀번호가 올바르지 않습니다.");
                idChangePw.focus();
                return;
            } else {
                alert("아이디가 변경되었습니다.")
                newID.value = ""
                idChangePw.value = ""
                closePopup(false, "nothing")
                return;
            }
        },
        error: function (request, status, error) {
            console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            // ajax 처리가 결과가 에러이면 전송 여부는 false // 앞서 초기값을 false로 해 놓았지만 한번 더 선언을 한다.
        }
    });
}