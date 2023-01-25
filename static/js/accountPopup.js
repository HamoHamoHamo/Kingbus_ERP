const HomePopupAreaModules = document.querySelectorAll(".HomePopupAreaModules")
const HomePopupBgModules = document.querySelectorAll(".HomePopupBgModules")
const HomeCloseBtn = document.querySelectorAll(".HomeCloseBtn")
const profileMenuCell = document.querySelectorAll(".profileMenuCell")
const HomeEditBtn = document.querySelectorAll(".HomeEditBtn")
const username_input= document.querySelector('.username_input');
const PopupDataInputPwCheckerId = document.querySelector('.PopupDataInputPwCheckerId');
const PopupDataInputPwCheckerPw = document.querySelector('.PopupDataInputPwCheckerPw');
const PopupDataInputNewPw = document.querySelector('.PopupDataInputNewPw');
const PopupDataInputOverlap = document.querySelector('.PopupDataInputOverlap');


//아이디 수정  팝업
profileMenuCell[0].addEventListener('click', openIDPopup)

function openIDPopup() {
    HomePopupAreaModules[0].style.display = "block"
    PopupDataInputPwCheckerId.value = ""
    username_input.value = ""
    profileBox.style.display = "none"

}

//아이디 수정
HomeEditBtn[0].addEventListener('click', idChecker)

function idChecker() {
    if (username_input.attributes.check_result.value == "fail" || PopupDataInputPwCheckerId.value == "") {
        if (PopupDataInputPwCheckerId.value == "") {
            alert("비밀번호가 입력되지 않았습니다.")
        } else if (username_input.attributes.check_result.value == "fail") {
            alert("아이디 중복확인이 되지 않았습니다.")
        }
    } else {
        pw_overlap_check_id()
    }
}

//csrf token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

let csrftoken = getCookie('csrftoken');

// 아이디 중복검사
function id_overlap_check() {

    $('.username_input').change(function () {
        $('.username_input').attr("check_result", "fail");
    })


    if ($('.username_input').val() == '') {
        alert('아이디를 입력해주세요.')
        return;
    }


    $.ajax({
        url: "/member/id-check",
        data: {
            'user_id': username_input.value
        },
        datatype: 'json',
        success: function (data) {
            console.log(data['overlap']);
            if (data['overlap'] == "fail") {
                alert("이미 존재하는 아이디 입니다.");
                username_input.focus();
                return;
            } else {
                alert("사용가능한 아이디 입니다.");
                $('.username_input').attr("check_result", "success");
                return;
            }
        },
        error: function (request, status, error) {
            console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            // ajax 처리가 결과가 에러이면 전송 여부는 false // 앞서 초기값을 false로 해 놓았지만 한번 더 선언을 한다.
        }
    });
}


// 비밀번호 비교(아이디 수정)
function pw_overlap_check_id() {

    $('.PopupDataInputPwCheckerId').change(function () {
        $('.PopupDataInputPwCheckerId').attr("check_result", "fail");
    })


    if ($('.PopupDataInputPwCheckerId').val() == '') {
        alert('비밀번호를 입력해주세요.')
        return;
    }


    $.ajax({
        url: "/member/change/id",
        method: "POST",
        data: {
            'user_id': username_input.value,
            'password': PopupDataInputPwCheckerId.value,
            'csrfmiddlewaretoken': csrftoken,
            'X-CSRFToken': csrftoken
        },
        datatype: 'json',
        success: function (data) {
            if (data['status'] == "fail") {
                alert("비밀번호가 올바르지 않습니다.");
                PopupDataInputPwCheckerId.focus();
                return;
            } else {
                alert("아이디가 변경되었습니다.")
                closeHomePopup()
                return;
            }
        },
        error: function (request, status, error) {
            console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            // ajax 처리가 결과가 에러이면 전송 여부는 false // 앞서 초기값을 false로 해 놓았지만 한번 더 선언을 한다.
        }
    });
}


//비밀번호 수정  팝업
profileMenuCell[1].addEventListener('click', openPWPopup)

function openPWPopup() {
    HomePopupAreaModules[1].style.display = "block"
    PopupDataInputPwCheckerPw.value = ""
    PopupDataInputNewPw.value = ""
    PopupDataInputOverlap.value = ""
    profileBox.style.display = "none"
}


//비밀번호 수정
HomeEditBtn[1].addEventListener('click', pwChecker)

function pwChecker() {
    if (PopupDataInputPwCheckerPw.value == "" || PopupDataInputNewPw.value == "" || PopupDataInputOverlap.value == "" || PopupDataInputNewPw.value !== PopupDataInputOverlap.value) {
        if (PopupDataInputPwCheckerPw.value == "" || PopupDataInputNewPw.value == "" || PopupDataInputOverlap.value == "") {
            alert("모든 항목을 입력해야 변경이 가능합니다.")
        } else if (PopupDataInputNewPw.value !== PopupDataInputOverlap.value) {
            alert("같은 비밀번호를 입력해주세요.")
        }
    } else {
        pw_overlap_check_pw()
    }
    return
}

// 비밀번호 비교(비밀번호 수정)
function pw_overlap_check_pw() {

    $('.PopupDataInputPwCheckerPw').change(function () {
        $('.PopupDataInputPwCheckerPw').attr("check_result", "fail");
    })


    if ($('.PopupDataInputPwCheckerPw').val() == '') {
        alert('비밀번호를 입력해주세요.')
        return;
    }


    $.ajax({
        url: "/member/change/password",
        method: "POST",
        data: {
            'cur_password': PopupDataInputPwCheckerPw.value,
            'password1': PopupDataInputNewPw.value,
            'password2': PopupDataInputOverlap.value,
            'csrfmiddlewaretoken': csrftoken
        },
        datatype: 'json',
        success: function (data) {
            console.log(data)
            if (data['status'] == "fail") {
                alert("비밀번호가 올바르지 않습니다.");
                PopupDataInputPwCheckerId.focus();
                return;
            } else {
                alert("비밀번호가 변경되었습니다.")
                closeHomePopup()
                return;
            }
        },
        error: function (request, status, error) {
            console.log("CODE:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            // ajax 처리가 결과가 에러이면 전송 여부는 false // 앞서 초기값을 false로 해 놓았지만 한번 더 선언을 한다.
        }
    });
}

//팝업닫기
for (i = 0; i < HomePopupBgModules.length; i++) {
    HomePopupBgModules[i].addEventListener("click", closeHomePopup)
    HomeCloseBtn[i].addEventListener("click", closeHomePopup)
}

function closeHomePopup() {
    for (i = 0; i < HomePopupAreaModules.length; i++) {
        HomePopupAreaModules[i].style.display = "none"
    }
}