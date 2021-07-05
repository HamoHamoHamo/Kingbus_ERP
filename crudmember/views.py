from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login
from .models import User, UserFile
from string import ascii_lowercase
from random import choice


def home(request):
    user_id = request.session.get('user')
    if user_id:
        user_info = User.objects.get(pk=user_id)
        context = {
            "name" : user_info.name,
        }
        return render(request, 'crudmember/home.html', context)
    return redirect('crudmember:login')

def signup_terms(request):
    return render(request, 'crudmember/signup_terms.html')

def signup(request):
    if request.method == "GET":
        return render(request, 'crudmember/signup.html')

    elif request.method == 'POST':
        userid = request.POST.get('userid', None)
        password1 = request.POST.get('password1', None)
        password2 = request.POST.get('password2', None)
        name = request.POST.get('name', None)
        tel = request.POST.get('tel', None)
        photo = request.FILES.get('photo', None)
        files = request.FILES.getlist('file')
        res_data = {}
        if User.objects.filter(userid=userid).exists(): #아이디 중복체크
            res_data['error'] = '사용중인 아이디입니다.'
        elif password1 != password2:
            res_data['error'] = "비밀번호가 다릅니다."
        else:
            user = User(
                userid = userid, 
                password = make_password(password1),
                name = name,
                tel = tel,
                photo = photo
                )
            user.save()

            for upload_file in files:
                user_file = UserFile(
                    user_id=get_object_or_404(User, userid=userid),
                    file=upload_file
                )
                user_file.save()
            #auth.login(request, user)
            return render(request, 'crudmember/login.html', res_data)
        return render(request, 'crudmember/signup.html', res_data)
        

def login(request):
    # 로그인 기능
    res_data = {}
    if request.method == 'POST':
        login_username = request.POST.get('userid', None)
        login_password = request.POST.get('password', None)
        
        try:
            user = User.objects.get(userid=login_username)
        except Exception as e:
            print("error", e)
            res_data['error'] = "아이디/비밀번호가 다릅니다."
            return render(request, 'crudmember/login.html', res_data)
            
        if check_password(login_password, user.password):
            request.session['user'] = user.id
            request.session['name'] = user.name

                #세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
                #세션 user라는 key에 방금 로그인한 id를 저장한것.
            return redirect('/')
        else:
            res_data['error'] = "아이디/비밀번호가 다릅니다."
            print("비밀번호다름")
            return render(request, 'crudmember/login.html', res_data)
    else:
        user_id = request.session.get('user')
        if user_id:
            return redirect('home')
        return render(request, 'crudmember/login.html')


def logout(request):
    request.session.pop('user')
    request.session.pop('name')
    return redirect('/')


def profile(request):
    res_data = {}
    if request.method == 'GET':
        return render(request, 'crudmember/profile.html')
    if request.method == 'POST':
        # user_id = request.session.get('user')
        # 비밀번호 변경폼
        if 'cngpw' in request.POST:
            user = User.objects.get(pk=request.session.get('user'))
            oldpw = request.POST.get('old_password', None)
            if check_password(oldpw, user.password):
                newpw = request.POST.get('new_password1', None)
                newpw2 = request.POST.get('new_password2', None)
                if newpw == newpw2:
                    if len(newpw) >= 4:
                        user.password = make_password(newpw)
                        user.save()
                        # login(request, user)
                    else:
                        res_data['error'] = "길이 너무 짧음"
                        return render(request, 'crudmember/profile.html', res_data)
                else:
                    res_data['error'] = "1,2틀림"
                    return render(request, 'crudmember/profile.html', res_data)
            else:
                res_data['error'] = "old비번틀림"
                return render(request, 'crudmember/profile.html', res_data)
        return redirect('home')


def passwordfinder(request):
    res_data={}
    if request.method == 'GET':
        return render(request, 'crudmember/passwordfinder.html')  # return redirect('passwordfinder')
    if request.method == 'POST':
        if 'findpw' in request.POST:
            userid = request.POST.get('userid', None)
            name = request.POST.get('name', None)
            tel = request.POST.get('tel', None)
            try:
                user = User.objects.get(userid = userid)
            except Exception:
                res_data['error'] = "아이디없음"
                return render(request, 'crudmember/passwordfinder.html', res_data)
            if user.name == name:
                if str(user.tel) == tel:  # tel을 숫자로받아야함 (임시)
                    result = ""    # 난수생성해서 비번초기화하기
                    for i in range(4):
                        result += choice(ascii_lowercase)
                    user.password = make_password(result)
                    user.save()
                    res_data['error'] = "비밀번호 초기화 완료 : " + result
                    return render(request, 'crudmember/passwordfinder.html', res_data)
                else:
                    res_data['error'] = "번호없음"
                    return render(request, 'crudmember/passwordfinder.html', res_data)
            else:
                res_data['error'] = "이름없음"
                return render(request, 'crudmember/passwordfinder.html', res_data)

