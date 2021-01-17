from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from .models import Notice, NoticeFile, NoticeComment
'''
class NoticeKindsView(generic.ListView):
    model = Notice
    template_name = 'notice/kinds.html'
    context_object_name = 'notices'

    #paginate_by = 2
    #한 페이지에 보여주는 객체 리스트의 갯수 지정
'''
def kinds(request, kinds):
    kinds_check(kinds)
    context = {
        'notices': Notice.objects.all().filter(kinds=kinds),
        'kinds':kinds,
    }
    return render(request, 'notice/kinds.html', context)

def create(request):
    if request.method == "GET":
        return render(request, 'notice/create.html')

    elif request.method == 'POST':
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        kinds = request.POST.get('kinds', None)
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
    return render(request, 'notice/create.html')

def detail(request, kinds, question_id):
    kinds_check(kinds)
    return render(request, 'notice/detail.html')

def delete(request, kinds, question_id):
    kinds_check(kinds)
    return redirect('/notice/{0}/'.format(kinds))

def kinds_check(kinds): # driver 나 office인지 체크
    if kinds != "driver" and kinds != "office":
        raise Http404