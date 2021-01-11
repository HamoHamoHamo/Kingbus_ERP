from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import auth

def home(request):
    if request.method == 'POST':
        res_data = {}
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            print("테스트")
            res_data['error'] = "아이디/비밀번호가 다릅니다."
            return render(request, 'crudmember/home.html', res_data)
    else:
        return render(request, 'crudmember/home.html')

def signup(request):
    if request.method == "GET":
        return render(request, 'crudmember/signup.html')

    elif request.method == 'POST':
        User = get_user_model()
        User.objects.all()
        username = request.POST.get('username',None)
        password1 = request.POST['password1']
        password2 = request.POST.get('password2',None)
        res_data = {}
        if password1 != password2:
            res_data['error'] = "비밀번호가 다릅니다."
        else:
            user = User.objects.create_user(
                username, password1
            )
            #auth.login(request, user)
        return render(request, 'crudmember/signup.html', res_data)

def login(request):
    if request.method == 'POST':
        res_data = {}
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            print("테스트")
            res_data['error'] = "아이디/비밀번호가 다릅니다."
            return render(request, 'crudmember/home.html', res_data)
    else:
        return render(request, 'crudmember/home.html')

def logout(request):
    auth.logout(request)
    return redirect('home')
