from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import BadRequest
from django.http import Http404, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.views import generic

from .models import User, UserFile, Category, Client
from .forms import UserForm, ClientForm
from humanresource.models import Member, Salary
from dispatch.models import Schedule, DispatchCheck, DispatchOrder, DispatchOrderConnect, DispatchRegularly, DispatchRegularlyData, DispatchRegularlyConnect
from vehicle.models import Vehicle
from dispatch.views import FORMAT, TODAY
from dateutil.relativedelta import relativedelta

from datetime import datetime, timedelta
from random import choice
from string import ascii_lowercase


# from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from .tokens import account_activation_token

WEEK = ['월', '화', '수', '목', '금', '토', '일']
def sunghwatour_rule(request):
    return render(request, 'crudmember/sunghwatour_rule.html')


class CategoryList(generic.ListView):
    template_name = 'crudmember/setting.html'
    context_object_name = 'category_list'
    model = Category

    def get(self, request, *args, **kwargs):
        if request.session.get('authority') > 2:
            return render(request, 'authority.html')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        category_list = context['category_list']

        vehicle_type_list = []
        operation_type_list = []
        order_type_list = []
        bill_place_list = []
        reservation_list = []
        operating_list = []

        for category in category_list:
            if category.type == '차량종류':
                vehicle_type_list.append(category)
            elif category.type == '운행종류':
                operation_type_list.append(category)
            elif category.type == '유형':
                order_type_list.append(category)
            elif category.type == '계산서 발행처':
                bill_place_list.append(category)
            elif category.type == '예약회사':
                reservation_list.append(category)
            elif category.type == '운행회사':
                operating_list.append(category)
            elif category.type == '식대':
                context['meal'] = category.category
            elif category.type == '급여지급일':
                context['payment_date'] = category.category
        
        context['vehicle_type_list'] = vehicle_type_list
        context['operation_type_list'] = operation_type_list
        context['order_type_list'] = order_type_list
        context['bill_place_list'] = bill_place_list
        context['reservation_list'] = reservation_list
        context['operating_list'] = operating_list

        

        return context


def setting_create(request):
    if request.method == 'POST':
        if request.session.get('authority') > 2:
            return render(request, 'authority.html')
    
        type = request.POST.get('type')
        category = request.POST.get('category')
        creator = get_object_or_404(Member, pk=request.session.get('user'))

        category = Category(
            type = type,
            category = category,
            creator = creator
        )
        category.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    else:
        return HttpResponseNotAllowed(['post'])

def setting_delete(request):
    if request.method == 'POST':
        if request.session.get('authority') > 2:
            return render(request, 'authority.html')
        id_list = request.POST.getlist('check')

        for id in id_list:
            category = Category.objects.get(id=id)
            category.delete()
        
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    else:
        return HttpResponseNotAllowed(['post'])


class ClientList(generic.ListView):
    template_name = 'crudmember/setting_client.html'
    context_object_name = 'client_list'
    model = Client

    def get(self, request, *args, **kwargs):
        if request.session.get('authority') > 3:
            return render(request, 'authority.html')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        select = self.request.GET.get('select', '')
        search = self.request.GET.get('search', '')

        if select == '거래처명' and search:
            client_list = Client.objects.filter(name__contains=search).order_by('name')
        elif select == '대표자명' and search:
            client_list = Client.objects.filter(representative__contains=search).order_by('name')
        elif select == '담당자명' and search:
            client_list = Client.objects.filter(manager__contains=search).order_by('name')
        else:
            client_list = Client.objects.all().order_by('name')

        return client_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['select'] = self.request.GET.get('select', '')
        context['search'] = self.request.GET.get('search', '')


        context['data_list'] = []
        for client in context['client_list']:
            context['data_list'].append({
                'business_num': client.business_num,
                'name': client.name,
                'representative': client.representative,
                'phone': client.phone,
                'manager': client.manager,
                'manager_phone': client.manager_phone,
                'email': client.email,
                'address': client.address,
                'note': client.note,
                'id': client.id,
            })

        return context


def setting_client_create(request):
    if request.method == 'POST':
        if request.session.get('authority') > 3:
            return render(request, 'authority.html')
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            creator = get_object_or_404(Member, pk=request.session.get('user'))

            client = client_form.save(commit=False)
            client.creator = creator
            client.save()
        
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            raise BadRequest

    else:
        return HttpResponseNotAllowed(['post'])

def setting_client_edit(request):
    if request.method == 'POST':
        if request.session.get('authority') > 3:
            return render(request, 'authority.html')
        client_id = request.POST.get('id')
        client = get_object_or_404(Client, id=client_id)

        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            client.business_num = client_form.cleaned_data['business_num']
            client.name = client_form.cleaned_data['name']
            client.representative = client_form.cleaned_data['representative']
            client.phone = client_form.cleaned_data['phone']
            client.manager = client_form.cleaned_data['manager']
            client.manager_phone = client_form.cleaned_data['manager_phone']
            client.email = client_form.cleaned_data['email']
            client.address = client_form.cleaned_data['address']
            client.note = client_form.cleaned_data['note']
            client.save()
        
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            raise BadRequest

    else:
        return HttpResponseNotAllowed(['post'])

def setting_client_delete(request):
    if request.method == 'POST':
        if request.session.get('authority') > 3:
            return render(request, 'authority.html')
        id_list = request.POST.getlist('check')

        for id in id_list:
            client = Client.objects.get(id=id)
            client.delete()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    else:
        return HttpResponseNotAllowed(['post'])



def salary_date(request):
    if request.method == 'POST':
        payment_date = request.POST.get('payment_date')
        date = request.POST.get('date')
        try:
            category = Category.objects.get(type='급여지급일')
            category.category = payment_date
        except Category.DoesNotExist:
            category = Category(
                type = '급여지급일',
                category = payment_date,
            )
        category.save()

        salary_list = Salary.objects.filter(month__gte=date)
        for salary in salary_list:
            salary.payment_date = payment_date
            salary.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def home(request):
    id = request.session.get('user')
    if id:
        user_info = User.objects.get(pk=id)
        context = {
            "name" : user_info.name,
        }
        return render(request, 'crudmember/home.html', context)
    return redirect('crudmember:login')

class Calendar(generic.ListView):
    template_name = 'crudmember/home.html'
    context_object_name = 'order_list'
    model = DispatchOrder

    def get_queryset(self):
        return 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.request.GET.get('year', TODAY[:4])
        month = self.request.GET.get('month', TODAY[5:7])

        # ?
        # if self.request.GET.get('change') == 'true':
        #     DispatchOrder.objects.filter(departure_date__startswith=f'{year}-{month}').exclude(contract_status='취소')
                    
        weekday_list = [
            datetime.strptime(f'{year}-{month}-01', FORMAT),
            datetime.strptime(f'{year}-{month}-02', FORMAT),
            datetime.strptime(f'{year}-{month}-03', FORMAT),
            datetime.strptime(f'{year}-{month}-04', FORMAT),
            datetime.strptime(f'{year}-{month}-05', FORMAT),
            datetime.strptime(f'{year}-{month}-06', FORMAT),
            datetime.strptime(f'{year}-{month}-07', FORMAT),
        ]
        last_day = datetime.strftime(weekday_list[0] + relativedelta(months=1) - timedelta(days=1), FORMAT)[8:]

        total_bus_cnt = [0] * int(last_day)
        cur_bus_cnt = [0] * int(last_day)

        r_total_bus_cnt = [0] * int(last_day)
        r_cur_bus_cnt = [0] * int(last_day)

        check_list = [''] * int(last_day)
        schedule_list = [''] * int(last_day)

        change_order_list = [''] * int(last_day)

        
        dispatch_list = DispatchOrder.objects.prefetch_related('info_order').filter(departure_date__startswith=f'{year}-{month}').exclude(contract_status='취소')
        regularly_list = DispatchRegularlyConnect.objects.filter(departure_date__startswith=month)

        for dispatch in dispatch_list:
            departure_date = datetime.strptime(dispatch.departure_date[:10], FORMAT)
            arrival_date = datetime.strptime(dispatch.arrival_date[:10], FORMAT)
            days = (arrival_date - departure_date).days + 1
            
            temp_list = []
            for i in range(days):
                date = int(datetime.strftime(departure_date, FORMAT)[8:10])
                total_bus_cnt[date-1] += int(dispatch.bus_cnt)
                cur_bus_cnt[date-1] += dispatch.info_order.all().count()

                # 배차달력 노선별 버스 대수
                temp_list.append
                if not isinstance(change_order_list[date-1], list): change_order_list[date-1] = []
                change_order_list[date-1].append({
                    'customer': dispatch.customer,
                    'cnt': dispatch.bus_cnt
                })
                departure_date += timedelta(days=1)

        
        cnt = 0
        for day in weekday_list:
            cnt += 1
            weekday = WEEK[day.weekday()]
            regularly_cnt = DispatchRegularlyData.objects.filter(use='사용').filter(week__contains=weekday).count()
            cnt_day = 0
            while(cnt+cnt_day <= int(last_day)):
                #
                roof_date = cnt + cnt_day
                if roof_date < 10:
                    roof_date = f'0{roof_date}'
                
                
                schedules = Schedule.objects.filter(date=f'{year}-{month}-{roof_date}')
                temp_list = []
                for sch in schedules:
                    temp_list.append({
                        'content': sch.content,
                        'date': datetime.strftime(sch.pub_date, FORMAT),
                        'id': sch.id,
                        'creator': sch.creator.name,
                    })
                if temp_list:
                    schedule_list[cnt+cnt_day-1] = temp_list

                r_total_bus_cnt[cnt+cnt_day-1] += regularly_cnt

                cnt_day += 7
        
        regularly_list = DispatchRegularlyConnect.objects.filter(departure_date__startswith=f'{year}-{month}')
        for regularly in regularly_list:
            date = int(regularly.departure_date[8:10])
            r_cur_bus_cnt[date-1] += 1


        # print("TT", total_bus_cnt)
        # print("CC", cur_bus_cnt)
        # print("RRRRRRRRRT", r_total_bus_cnt)
        # print("RCC", r_cur_bus_cnt)
        context['schedule_list'] = schedule_list
        context['total_bus_cnt'] = total_bus_cnt
        context['cur_bus_cnt'] = cur_bus_cnt
        context['r_total_bus_cnt'] = r_total_bus_cnt
        context['r_cur_bus_cnt'] = r_cur_bus_cnt
        context['change_order_list'] = change_order_list


        
        next_month = (datetime.strptime(TODAY, FORMAT) + relativedelta(months=1)).strftime(FORMAT)
        context['vehicle_list'] = Vehicle.objects.filter(check_date__range=(TODAY, next_month))
        

        checks = DispatchCheck.objects.filter(date__startswith=f'{year}-{month}').order_by('date')
        for check in checks:
            creator = check.creator.name if check.creator else ''
            check_list[int(check.date[8:])-1] = {
                'creator': creator,
                'date': datetime.strftime(check.updated_at, f'{FORMAT} %H:%M'),
            }
            
        context['check_list'] = check_list
        return context

def reset_password(request):
    id = request.GET.get('id')
    if id:
        member = get_object_or_404(Member, id=id)
        member.password = make_password('0000')
        member.save()

        return redirect('crudmember:signup_terms')
    else:
        raise Http404


def signup_terms(request):
    return render(request, 'crudmember/signup_terms.html')

def welcome(request):
    return render(request, 'crudmember/welcome.html')

def id_overlap_check(request):
    if request.method == "GET":
        user_id = request.GET.get('user_id')
        try:
            # 중복 검사 실패
            user = Member.objects.get(user_id=user_id)
        except:
            # 중복 검사 성공
            user = None
        if user is None:
            overlap = "pass"
        else:
            overlap = "fail"
        context = {'overlap': overlap}
        return JsonResponse(context)
    else:
        return JsonResponse({'error': 'method not allowed'})

def change_id(request):
    if request.method == "POST":
        password = request.POST.get('password')
        member = get_object_or_404(Member, id=request.session.get('user'))

        if check_password(password, member.password):
            change_id = request.POST.get('user_id')
            if change_id:
                member.user_id = change_id
                member.save()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({"status": "fail"})
        return JsonResponse({"status": "fail"})
    return JsonResponse({"status": "fail"})

def change_password(request):
    if request.method == "POST":
        cur_password = request.POST.get('cur_password')
        member = get_object_or_404(Member, id=request.session.get('user'))

        if check_password(cur_password, member.password):
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == password2:
                member.password = make_password(password1)
                member.save()
                return JsonResponse({"status": 'success'})
            else:
                return JsonResponse({"status": 'fail'})

        return JsonResponse({"status": "fail"})
    return JsonResponse({"error": "method not allowed", "status": "fail"})
    

def signup(request):
    if request.method == "GET":
        form = UserForm

        return render(request, 'crudmember/signup.html', {
            'form': form,
        })

    elif request.method == 'POST':
        user_form = UserForm(request.POST)
        
        user_id = request.POST.get('user_id', None)
        password1 = request.POST.get('password1', None)
        password2 = request.POST.get('password2', None)
        files = request.FILES.getlist('file')
        mail = ''.join(request.POST.getlist('manager_mail', None))

        res_data = {}

        if User.objects.filter(user_id=user_id).exists(): #아이디 중복체크
            res_data['error'] = '사용중인 아이디입니다.'
        elif password1 != password2:
            res_data['error'] = "비밀번호가 다릅니다."
        elif user_form.is_valid():
            user = user_form.save(commit=False)
            user.password = make_password(password1)
            user.manager_mail = mail
            user.save()

            for upload_file in files:
                user_file = UserFile(
                    user_id=get_object_or_404(User, user_id=user_id),
                    file=upload_file
                )
                user_file.save()
            #auth.login(request, user)
            return render(request, 'crudmember/welcome.html', res_data)
        return render(request, 'crudmember/signup.html', res_data)
        

def login(request):
    # 로그인 기능
    res_data = {}
    if request.method == 'POST':
        login_username = request.POST.get('userid', None)
        login_password = request.POST.get('password', None)
        
        try:
            user = Member.objects.get(user_id=login_username)
        except Exception as e:
            res_data['error'] = "아이디/비밀번호가 다릅니다"
            return render(request, 'crudmember/login.html', res_data)
        
        if user.role == '임시' or user.use == '삭제' or user.use == '미사용':
            res_data['error'] = "접근 권한이 없습니다"
            return render(request, 'crudmember/login.html', res_data)
        if check_password(login_password, user.password):
            request.session['user'] = user.id
            request.session['name'] = user.name
            request.session['authority'] = user.authority
            # request.session['login_time'] = str(datetime.now())[:16]
            # request.session['today'] = str(datetime.now())[:10]
            #세션 만료시간 설정 0을 넣으면 브라우져 닫을시 세션 쿠키 삭제 + DB만료기간 14일
            if request.POST.get('auto_login'):
                request.session.set_expiry(2592000)
                # 30일 초로 변환
            else:
                request.session.set_expiry(0)
            

                #세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
                #세션 user라는 key에 방금 로그인한 id를 저장한것.
            return redirect('home')
        else:
            res_data['error'] = "아이디/비밀번호가 다릅니다."
            return render(request, 'crudmember/login.html', res_data)
    else:
        user_id = request.session.get('user')
        try:
            Member.objects.get(id=user_id)
            return redirect('home')
        except:
            return render(request, 'crudmember/login.html')


def logout(request):
    try:
        request.session.flush()
    except KeyError:
        pass
    return redirect('home')


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
                if user.tel == str(tel):  # tel을 숫자로받아야함 (임시)
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
            
        if 'sendemail' in request.POST:
            userid = request.POST.get('userid', None)
            useremail = request.POST.get('useremail', None)
            try:
                user = User.objects.get(userid = userid)
            except Exception:
                res_data['error'] = "아이디없음"
                return render(request, 'crudmember/passwordfinder.html', res_data)
            current_site = get_current_site(request)
            message = render_to_string('crudmember/user_passwordfinder_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = "패스워드 변경 메일입니다."
            user_toemail = useremail
            email = EmailMessage(mail_subject, message, to=[user_toemail])
            email.send()
            return HttpResponse(
                '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
                'justify-content: center; align-items: center;">'
                '입력하신 이메일<span>로 인증 링크가 전송되었습니다.</span>'
                '</div>'
            )
            return redirect('home')


# def pwchangeauth(request, uid64, token):

#     uid = force_text(urlsafe_base64_decode(uid64))
#     user = User.objects.get(pk=uid)

#     if user is not None and account_activation_token.check_token(user, token):
#         res_data = {}
#         if request.method == 'GET':
#             return render(request, 'crudmember/passwordchangeauth.html')
#             # return redirect('home')
#         if request.method == 'POST':
#             newpw = request.POST.get('new_password1', None)
#             newpw2 = request.POST.get('new_password2', None)
#             if newpw == newpw2:
#                 if len(newpw) >= 4:
#                     user.password = make_password(newpw)
#                     user.save()
#                     # login(request, user)
#                 else:
#                     res_data['error'] = "길이 너무 짧음"
#                     return render(request, 'crudmemeber/passwordchangeauth.html', res_data)
#             else:
#                 res_data['error'] = "1,2틀림"
#                 return render(request, 'crudmemeber/passwordchangeauth.html', res_data)
#         return redirect('home')
#     else:
#         return HttpResponse('비정상적인 접근입니다.')