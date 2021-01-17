from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from .models import User, UserFile

def home(request):
    user_id = request.session.get('user')
    if user_id:
        user_info = User.objects.get(pk=user_id)
        context = {
            "name" : user_info.name,
        }
        return render(request, 'crudmember/home.html', context)
    return redirect('crudmember:login')


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
        
        user = User.objects.get(userid=login_username)
        if check_password(login_password, user.password):
            request.session['user'] = user.id 

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
    return redirect('/')
