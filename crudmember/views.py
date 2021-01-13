from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import User

def home(request):
    user_id = request.session.get('user')
    print(user_id)
    if user_id:
        user_info = User.objects.get(pk=user_id)
        context = {
            "username" : user_info.username,
            "password" : user_info.password
        }
        return render(request, 'crudmember/home.html', context)
    return redirect('crudmember:login')


def signup(request):
    if request.method == "GET":
        return render(request, 'crudmember/signup.html')

    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password1 = request.POST.get('password1', None)
        password2 = request.POST.get('password2', None)
        res_data = {}
        if password1 != password2:
            res_data['error'] = "비밀번호가 다릅니다."
        else:
            user = User(username=username, password=make_password(password1))
            user.save()            
            #auth.login(request, user)
        return render(request, 'crudmember/login.html', res_data)

def login(request):
    print('로그인')
    # 로그인 기능
    res_data = {}
    if request.method == 'POST':
        login_username = request.POST.get('username', None)
        login_password = request.POST.get('password', None)
        
        user = User.objects.get(username=login_username)
        if check_password(login_password, user.password):
            print("패스워드 체크")
            request.session['user'] = user.id 
                #세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
                #세션 user라는 key에 방금 로그인한 id를 저장한것.
            return redirect('/')
        else:
            res_data['error'] = "아이디/비밀번호가 다릅니다."
            print("비밀번호다름")
            return render(request, 'crudmember/login.html', res_data)
    else:
        return render(request, 'crudmember/login.html')


def logout(request):
    request.session.pop('user')
    return redirect('/')
