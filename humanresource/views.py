import pandas as pd
import json
import mimetypes
import os
import urllib
from config.settings import MEDIA_ROOT
from dateutil.relativedelta import relativedelta
from dispatch.models import DispatchRegularlyConnect, DispatchOrderConnect
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Sum, Q, F
from django.http import Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import resolve
from django.views import generic
from enum import Enum
from config.settings import FORMAT
from datetime import datetime, timedelta
from config.settings import BASE_DIR
from crudmember.models import Category
from vehicle.models import Vehicle
from .forms import MemberForm
from .models import Member, MemberFile, Salary, AdditionalSalary, DeductionSalary, Team
from accounting.models import TotalPrice
from assignment.models import AssignmentConnect
import math
from my_settings import CRED_PATH, CLOUD_MEDIA_PATH
from common.constant import TODAY, WEEK
from common.datetime import calculate_time_difference
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from media_firebase import upload_to_firebase, get_download_url, delete_firebase_file


def send_message(title, body, token, topic):
    cred_path = os.path.join(BASE_DIR, CRED_PATH)
    cred = credentials.Certificate(cred_path)
    
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    # Android 알림 설정
    android_config = messaging.AndroidConfig(
        notification=messaging.AndroidNotification(
            title=title,
            body=body,
            sound='kingbus.wav',  # 알림 소리 지정
            channel_id='DefaultChannel',
        )
    )

    
    # APNs 알림 설정
    apns_config = messaging.APNSConfig(
        payload=messaging.APNSPayload(
            aps=messaging.Aps(
                alert=messaging.ApsAlert(
                    title=title,
                    body=body,
                ),
                sound='KingbusAlarmSound.caf'  # 알림 소리 지정
            )
        )
    )
    message = messaging.Message(
        # android=android_config,
        apns=apns_config,
        token=token,
        topic=topic,
        data = {
            'title' : title,
            'body' : body,
            'sound' : 'kingbus.wav',  # 알림 소리 지정
        }
    )

    response = messaging.send(message)
    print('Successfully sent message:', response)


class MemberList(generic.ListView):
    template_name = 'HR/member.html'
    context_object_name = 'member_list'
    model = Member
    paginate_by = 10

    def get(self, request, **kwargs):
        if request.session.get('authority') >= 3:
            return render(request, 'authority.html')
        else:
            return super().get(request, **kwargs)

    def get_queryset(self):
        name = self.request.GET.get('name', '')
        age = self.request.GET.get('age', '나이')
        use = self.request.GET.get('use', '사용')
        role = self.request.GET.get('role', '담당업무')
        req_order_by = self.request.GET.get('order_by', 'name')
        
        up65 = f'{int(TODAY[:4]) - 65}{TODAY[4:10]}'

        authority = self.request.session.get('authority')
        
        if name:
            member_list = Member.objects.filter(use=use).filter(authority__gte=authority).filter(name__contains=name).order_by(req_order_by)
        else:
            member_list = Member.objects.filter(use=use).filter(authority__gte=authority).order_by(req_order_by)
        if age == '65세 이상':
            member_list = member_list.filter(birthdate__lte=up65)
        if role != '담당업무':
            member_list = member_list.filter(role=role)
        
        # if req_order_by == 'entering_date':
        #     print(member_list)
        #     member_list.order_by('entering_date')
        #     print(member_list)
        
        return member_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        #페이징 끝
        context['start_num'] = 1 + paginator.per_page * (current_page-1)

        member_list = context['member_list']
        data_list = []
        data_count_list = []
        file_list = []
        file_count_list = []
        
        for member in member_list:
            data_list.append({
                'name': member.name,
                'role': member.role,
                'birthdate': member.birthdate,
                'address': member.address,
                'phone_num': member.phone_num,
                'entering_date': member.entering_date,
                'id': member.user_id if member.user_id else '',
                'note': member.note,
                'user_id': member.id,
                'emergency': member.emergency,
                'use': member.use,
                'interview_date' : member.interview_date,
                'contract_date' : member.contract_date,
                'contract_renewal_date' : member.contract_renewal_date,
                'contract_condition' : member.contract_condition,
                'renewal_reason' : member.renewal_reason,
                'apply_path' : member.apply_path,
                'career' : member.career,
                'position' : member.position,
                'apprenticeship_note' : member.apprenticeship_note,
                'leave_reason' : member.leave_reason,
                'resident_number1' : member.resident_number1,
                'resident_number2' : member.resident_number2,
                'company' : member.company,
                'team' : member.team.name if member.team else '',
                'final_opinion' : member.final_opinion,
                'interviewer' : member.interviewer,
                'end_date' : member.end_date,
                'leave_date' : member.leave_date,
                'allowance_type' : member.allowance_type,
                'license' : member.license,
            })
            data_count = 0
            for key, value in data_list[-1].items():
                if key != 'birthdate' and key != 'allowance_type' and value != '' and value != " ":
                    data_count += 1
            # id, user_id, use 개수 빼줌
            data_count -= 3
            data_count_list.append(data_count)

            files = list(MemberFile.objects.filter(member_id=member).order_by('type').values('id', 'type', 'filename'))
            file_list.append(files)
            file_count_list.append(len(files))

        context['file_count_list'] = file_count_list
        context['file_list'] = file_list
        context['data_count_list'] = data_count_list
        context['data_list'] = data_list
        context['name'] = self.request.GET.get('name', '')
        context['role'] = self.request.GET.get('role', '담당업무')
        context['use'] = self.request.GET.get('use', '사용')
        context['age'] = self.request.GET.get('age', '나이')
        context['req_order_by'] = self.request.GET.get('order_by', 'name')
        context['member_all'] = Member.objects.order_by('name')
        context['team_list'] = Team.objects.all().order_by('name')
        return context

def calculate_birthdate_by_resident_number(number):
    birthdate = f'{number[:2]}-{number[2:4]}-{number[4:6]}'
    # 주민번호 앞에 19를 붙일지 20을 붙일지 확인
    if number > TODAY[2:4] + "0000":
        birthdate = "19" + birthdate
    else:
        birthdate = "20" + birthdate
    return birthdate

def member_create(request):
    if request.method == "POST":
        user_auth = request.session.get('authority')
        if user_auth >= 3:
            return render(request, 'authority.html')

        member_form = MemberForm(request.POST)
        if member_form.is_valid():
            role = request.POST.get('role')
            if role == '임시':
                req_auth = 5
            elif role == '용역':
                req_auth = 4
            elif role == '운전원':
                req_auth = 4
            elif role == '팀장':
                req_auth = 3
            elif role == '관리자':
                req_auth = 1
            elif role == '최고관리자':
                req_auth = 0
            
            if req_auth <= user_auth and user_auth != 0:
                return HttpResponseBadRequest()
            creator = Member.objects.get(pk=request.session.get('user'))
            member = member_form.save(commit=False)
            member.birthdate = calculate_birthdate_by_resident_number(member.resident_number1)
            member.company = request.POST.get('company', '')
            request_team = request.POST.get('team', '')
            try:
                team =Team.objects.get(id=request_team)
            except:
                team = None
            member.team = team
            member.creator = creator
            member.authority = req_auth
            user_id = request.POST.get('user_id', None)
            if req_auth != 5 and Member.objects.filter(user_id=user_id).exists(): #아이디 중복체크
                raise Http404
            
            if role != '임시':
                member.user_id = user_id
                member.password = make_password('0000')
            member.emergency = request.POST.get('emergency1', '') + ' ' + request.POST.get('emergency2', '')
            member.use = request.POST.get('use')
            member.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        print("ERRRRRRRRRRRR", member_form.errors)
        return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed(['post'])

def member_file_save(upload_file, member, type, creator):
    member_file = MemberFile(
        member_id=member,
        file=upload_file,
        filename=upload_file.name,
        type=type,
        creator=creator,
    )
    member_file.save()
    # print(vehicle_file)
    return member_file

def member_edit(request):
    if request.method == "POST":
        user_auth = request.session.get('authority')
        if user_auth >= 3:
            return render(request, 'authority.html')

        pk = request.POST.get('id', None)
        member = get_object_or_404(Member, pk=pk)

        member_form = MemberForm(request.POST)
        if member_form.is_valid():
            role = request.POST.get('role')
            if role == '임시':
                req_auth = 5
            elif role == '용역':
                req_auth = 4
            elif role == '운전원':
                req_auth = 4
            elif role == '팀장':
                req_auth = 3
            elif role == '관리자':
                req_auth = 1
            elif role == '최고관리자':
                req_auth = 0

            cur_auth = member.authority
            if user_auth != 0 and (req_auth == 0 or cur_auth == 0):
                return HttpResponseBadRequest('수정 권한이 없습니다')

            if member_form.cleaned_data['role'] == '운전원' and member.name != member_form.cleaned_data['name']:
                for vehicle in Vehicle.objects.filter(driver=member):
                    vehicle.driver_name = member_form.cleaned_data['name']
                    vehicle.save()
            member.name = member_form.cleaned_data['name']
            member.role = member_form.cleaned_data['role']
            member.entering_date = member_form.cleaned_data['entering_date']
            member.phone_num = member_form.cleaned_data['phone_num']
            member.address = member_form.cleaned_data['address']
            member.note = member_form.cleaned_data['note']
            member.interview_date = member_form.cleaned_data['interview_date']
            member.contract_date = member_form.cleaned_data['contract_date']
            member.contract_renewal_date = member_form.cleaned_data['contract_renewal_date']
            member.contract_condition = member_form.cleaned_data['contract_condition']
            member.renewal_reason = member_form.cleaned_data['renewal_reason']
            member.apply_path = member_form.cleaned_data['apply_path']
            member.career = member_form.cleaned_data['career']
            member.position = member_form.cleaned_data['position']
            member.apprenticeship_note = member_form.cleaned_data['apprenticeship_note']
            member.leave_reason = member_form.cleaned_data['leave_reason']
            member.license = member_form.cleaned_data['license']
            member.emergency = request.POST.get('emergency1', '') + ' ' + request.POST.get('emergency2', '')
            member.use = request.POST.get('use')
            member.authority = req_auth
            
            member.resident_number1 = request.POST.get('resident_number1')
            member.resident_number2 = request.POST.get('resident_number2')
            member.company = request.POST.get('company')
            request_team = request.POST.get('team', '')
            try:
                team =Team.objects.get(id=request_team)
            except:
                team = None
            member.team = team
            member.final_opinion = request.POST.get('final_opinion')
            member.interviewer = request.POST.get('interviewer')
            member.end_date = request.POST.get('end_date')
            member.leave_date = request.POST.get('leave_date')
            member.birthdate = calculate_birthdate_by_resident_number(member.resident_number1)
            member.allowance_type = request.POST.get('allowance_type', '기사수당(현재)')
            
            member.save()

            #### 금액, 기사수당 수정 시 입력한 월 이후 배차들 금액, 기사수당 수정
            post_month = request.POST.get('allowance_type_month')
            if post_month:
                day = '01'
                connect_list = DispatchRegularlyConnect.objects.filter(driver_id=member).filter(departure_date__gte=f'{post_month}-{day} 00:00').order_by('departure_date')
                for connect in connect_list:
                    month = connect.departure_date[:7]
                    regularly = connect.regularly_id

                    if connect.outsourcing == 'y':
                        allowance = regularly.outsourcing_allowance
                    else:
                        if connect.driver_id.allowance_type == '기사수당(변경)':
                            allowance = regularly.driver_allowance2
                        else:
                            allowance = regularly.driver_allowance

                    salary = Salary.objects.filter(member_id=member).get(month=month)
                    if connect.work_type == '출근':
                        salary.attendance = int(salary.attendance) + int(allowance) - int(connect.driver_allowance)
                    elif connect.work_type == '퇴근':
                        salary.leave = int(salary.leave) + int(allowance) - int(connect.driver_allowance)
                    salary.total = int(salary.total) + int(allowance) - int(connect.driver_allowance)
                    salary.save()

                    connect.driver_allowance = allowance
                    connect.save()
                
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            print(member_form.errors)
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed(['post'])

def member_delete(request):
    if request.method == 'POST':
        user_auth = request.session.get('authority')
        if user_auth >= 3:
            return render(request, 'authority.html')

        del_list = request.POST.getlist('delete_check', '')
        ####권한 확인
        
        for pk in del_list:
            req_auth = get_object_or_404(Member, pk=pk).authority
            if req_auth <= user_auth and user_auth != 0:
                return HttpResponseBadRequest()
        ####
        for pk in del_list:
            member = get_object_or_404(Member, pk=pk)
            vehicle_list = Vehicle.objects.filter(driver=member)
            for vehicle in vehicle_list:
                vehicle.driver_name = ''
                vehicle.save()
            member.use = '삭제'
            member.user_id = ''
            member.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

class DocumentType(Enum):
    RESUME = '이력서'
    CARPOOLING_AGREEMENT = '공동운행동의서'
    FAMILY_RELATIONS_CERTIFICATE = '등본'
    APPRENTICESHIP_CONTRACT = '견습계약서'
    EMPLOYMENT_CONTRACT = '근로계약서'
    COMPREHENSIVE_EVALUATION_SHEET = '종합판정표'
    BANK_STATEMENT = '통장사본'
    DRIVER_LICENSE = '운전면허증/버스자격증사본'
    HEALTH_CHECKUP_RESULTS = '건강검진결과'
    DRIVING_EXPERIENCE_CERTIFICATE = '운전경력증명서/경찰'
    OATH_DOCUMENT = '확약서'
    EXTENSION_OF_EMPLOYMENT_AGREEMENT = '연장근로동의서'
    PLEDGE_AGREEMENT = '서약서'
    SEXUAL_HARASSMENT_CONTRACT = '성희롱계약서'

def member_file_delete(id_list):
    for id in id_list:
        try:
            MemberFile.objects.get(id=id).delete()
        except:
            print("MemberFile delete error id : ", id)

def member_file_upload(request):
    user_auth = request.session.get('authority')
    if user_auth >= 3:
        return render(request, 'authority.html')

    if request.method == "GET":
        return HttpResponseNotAllowed(['POST'])

    creator = Member.objects.get(pk=request.session.get('user'))
    member = get_object_or_404(Member, id=request.POST.get('member_id'))

    for document_type in DocumentType:
        request_file = request.FILES.get(document_type.name, None)
        if request_file:
            try:
                old_file = MemberFile.objects.filter(member_id=member).get(type=document_type.value)
            except MemberFile.DoesNotExist:
                old_file = None

            print("test", old_file, document_type.name)
            file = member_file_save(request_file, member, document_type.value, creator)
            print("test22", old_file, document_type.name)
            try:
                file_path = f'{CLOUD_MEDIA_PATH}{file.file}_{file.filename}'
                upload_to_firebase(file, file_path)
                file.path = file_path
                file.save()
                os.remove(file.file.path)
            except Exception as e:
                print("Firebase upload error", e)
                #파이어베이스 업로드 실패 시 파일 삭제
                os.remove(file.file.path)
                file.delete()

            if old_file:
                #파이어베이스에서 예전 파일 삭제 / signals에서 삭제
                old_file.delete()
    
    delete_list = request.POST.getlist('delete_file_id', None)
    member_file_delete(delete_list)
    

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def member_file_download(request, file_id):
    user_auth = request.session.get('authority')
    if user_auth >= 3:
        return render(request, 'authority.html')
    file = get_object_or_404(MemberFile, id=file_id)
    context = {
        'url' : get_download_url(file.path)
    }
    return render(request, 'HR/member_img.html', context)

def member_download(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    datalist = list(Member.objects.exclude(use='삭제').order_by('name').values_list('id', 'user_id', 'name', 'role', 'birthdate', 'phone_num', 'emergency', 'address', 'entering_date', 'note', 'use', 'license'))
    
    try:
        df = pd.DataFrame(datalist, columns=['id', '사용자id', '이름', '업무', '생년월일', '전화번호', '비상연락망', '주소', '입사일', '비고', '사용여부', '버스기사자격증번호'])
        url = f'{MEDIA_ROOT}/humanresource/memberDataList.xlsx'
        df.to_excel(url, index=False)

        if os.path.exists(url):
            with open(url, 'rb') as fh:
                quote_file_url = urllib.parse.quote('직원목록.xlsx'.encode('utf-8'))
                response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(url)[0])
                response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
                return response
    except Exception as e:
        print(e)
        #return JsonResponse({'status': 'fail', 'e': e})
        raise Http404

class MemberEfficiencyList(generic.ListView):
    template_name = 'HR/member_efficiency.html'
    context_object_name = 'member_list'
    model = Member

    def get(self, request, **kwargs):
        if request.session.get('authority') >= 3:
            return render(request, 'authority.html')
        else:
            return super().get(request, **kwargs)

    def get_queryset(self):
        # route = self.request.GET.get('route', '')

        member_list = Member.objects.filter(use='사용').order_by('name')
        return member_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        FUEL = 1500         #기름값
        EFFICIENCY = 2.5    # 연비

        date1 = self.request.GET.get('date1', TODAY)
        date2 = self.request.GET.get('date2', TODAY)
        datetime1 = f'{date1} 00:00'
        datetime2 = f'{date2} 24:00'

        
        month = date1[:7] #  급여날짜 어떻게 할 지 확인 필요
        

        data_list = []
        for member in context['member_list']:
            data = {}
            # 급여
            try:
                salary = Salary.objects.filter(member_id=member).get(month=month)
            except Salary.DoesNotExist:
                creator = Member.objects.get(pk=self.request.session.get('user'))
                salary = new_salary(creator, month, member)
            

            # 노선운행량
            order_connect_list = member.info_driver_id.exclude(arrival_date__lt=datetime1).exclude(departure_date__gt=datetime2)
            regularly_connect_list = member.info_regularly_driver_id.exclude(arrival_date__lt=datetime1).exclude(departure_date__gt=datetime2)
            driving_history_list = member.driving_history_member.exclude(date__lt=date1).exclude(date__gt=date2).annotate(driving_distance=F('arrival_km') - F('departure_km'))
            
            price = 0
            minutes = 0
            distance = 0

            for connect in order_connect_list:
                price += int(connect.price)
                # distance += connect.order_id.distance
                minutes += calculate_time_difference(connect.departure_date, connect.arrival_date)

            for connect in regularly_connect_list:
                price += int(connect.price)
                distance += int(connect.regularly_id.distance) if connect.regularly_id.distance else 0
                minutes += calculate_time_difference(connect.departure_date, connect.arrival_date)

            data['driving_cnt'] = order_connect_list.count() + regularly_connect_list.count()
            data['price'] = price
            data['salary'] = salary.total
            data['distance'] = distance
            driving_distance = driving_history_list.aggregate(total_driving_distance=Sum('driving_distance'))['total_driving_distance']
            data['driving_distance'] = driving_distance if driving_distance else 0
            data['minute'] = minutes % 60
            data['hour'] = minutes // 60
            data['fuel_cost'] = data['driving_distance'] // EFFICIENCY * FUEL
            
            data_list.append(data)

            context['data_list'] = data_list
        return context

def member_route(request):

    return render(request, 'HR/member_route.html')


class TeamList(generic.ListView):
    template_name = 'HR/team.html'
    context_object_name = 'member_list'
    model = Member

    def get(self, request, **kwargs):
        if request.session.get('authority') >= 3:
            return render(request, 'authority.html')
        else:
            return super().get(request, **kwargs)

    def get_queryset(self):
        team = self.request.GET.get('team', '')
        name = self.request.GET.get('name', '')
        age = self.request.GET.get('age', '나이')
        use = self.request.GET.get('use', '사용')
        role = self.request.GET.get('role', '담당업무')
        team_none = self.request.GET.get('team_none', '')
        
        up65 = f'{int(TODAY[:4]) - 65}{TODAY[4:10]}'

        authority = self.request.session.get('authority')
        
        if name:
            member_list = Member.objects.exclude(Q(role="관리자")|Q(role="최고관리자")).filter(use=use).filter(authority__gte=authority).filter(name__contains=name).order_by("name")
        else:
            member_list = Member.objects.exclude(Q(role="관리자")|Q(role="최고관리자")).filter(use=use).filter(authority__gte=authority).order_by("name")
        if age == '65세 이상':
            member_list = member_list.filter(birthdate__lte=up65)
        if role != '담당업무':
            member_list = member_list.filter(role=role)
        if team:
            searched_team = get_object_or_404(Team, id=team)
            member_list = member_list.filter(team=searched_team)
        
        if team_none == "팀없음":
            member_list = member_list.filter(team=None)
        return member_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        team_id = self.request.GET.get('team', '')
        if team_id:
            team = get_object_or_404(Team, id=team_id)
        else:
            team = '전체'

        null = self.request.GET.get('team_none', '')
        if null == '팀없음':
            team = '팀없음'

        context['team_list'] = Team.objects.order_by('name')
        context['team'] = team
        context['name'] = self.request.GET.get('name', '')
        context['use'] = self.request.GET.get('use', '사용')
        context['role'] = self.request.GET.get('role', '담당업무')
        return context


def team_create(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "POST":
        team = Team(
            name = request.POST.get('name'),
        )
        team.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['POST'])

def team_edit(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "POST":
        id = request.POST.get('id', None)
        name = request.POST.get('name', None)
        team = get_object_or_404(Team, id=id)
        team.name = name
        team.save()
        
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['POST'])

def team_delete(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "POST":
        team = get_object_or_404(Team, id=request.POST.get('id', None))
        team.delete()
        return redirect('HR:team')
    else:
        return HttpResponseNotAllowed(['POST'])

def team_member(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

    if request.method == "POST":
        member_list = request.POST.getlist('id', None)
        team_list = request.POST.getlist('team_id', None)
        
        cnt = 0
        for member in member_list:
            member = get_object_or_404(Member, id=member)
            team_id = team_list[cnt]
            if team_id == 'none':
                member.team = None
            else:
                team = get_object_or_404(Team, id=team_id)
                member.team = team
            member.save()
            cnt += 1
        
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['POST'])


class SalaryList(generic.ListView):
    template_name = 'HR/salary_list.html'
    context_object_name = 'member_list'
    model = Member

    def get_queryset(self):
        month = self.request.GET.get('month', TODAY[:7])
        name = self.request.GET.get('name', '')

        authority = self.request.session.get('authority')
        if authority >= 3:
            id = self.request.session.get('user')
            member_list = Member.objects.filter(entering_date__lt=month+'-32').filter(id=id)
            return member_list
        else:
            member_list = Member.objects.filter(entering_date__lt=month+'-32').filter(use='사용').order_by('name')
            if name:
                member_list = member_list.filter(name__contains=name)
        
        view_name = resolve(self.request.path_info).url_name
        if view_name == 'salary':
            member_list = member_list.filter(Q(role='팀장')|Q(role='운전원')).filter(allowance_type='기사수당(현재)')
        elif view_name == 'salary_change':
            member_list = member_list.filter(Q(role='팀장')|Q(role='운전원')).filter(allowance_type='기사수당(변경)')
        elif view_name == 'salary_outsourcing':
            member_list = member_list.filter(Q(role='용역'))
        elif view_name == 'salary_manager':
            member_list = member_list.filter(Q(role='관리자'))
        else:
            raise HttpResponseBadRequest('url에러')
        return member_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        month = self.request.GET.get('month', TODAY[:7])
        name = self.request.GET.get('name', '')

        salary_list = []
        additional_list = []
        deduction_list = []
        year_list = []
        for member in context['member_list']:
            year = math.floor((datetime.strptime(TODAY[:10], FORMAT) - datetime.strptime(member.entering_date, FORMAT)).days/365)
            if year == 0:
                year = f'0{math.floor(((datetime.strptime(TODAY[:10], FORMAT) - datetime.strptime(member.entering_date, FORMAT)).days/30+0.5))}'
            year_list.append(year)

            try:
                salary = Salary.objects.filter(member_id=member).get(month=month)
            except Salary.DoesNotExist:
                creator = Member.objects.get(pk=self.request.session.get('user'))
                salary = new_salary(creator, month, member)
            
            salary_list.append(salary)

            ###########
            temp_add = []
            additionals = AdditionalSalary.objects.filter(member_id=member).filter(salary_id=salary)
            for additional in additionals:
                temp_add.append({
                    'price': additional.price,
                    'remark': additional.remark,
                    'id': additional.id,
                })
            additional_list.append(temp_add)

            temp_ded = []    
            deductions = DeductionSalary.objects.filter(member_id=member).filter(salary_id=salary)
            for deduction in deductions:
                temp_ded.append({
                    'price': deduction.price,
                    'remark': deduction.remark,
                    'id': deduction.id,
                })
            deduction_list.append(temp_ded)

        context['additional_list'] = additional_list
        context['deduction_list'] = deduction_list
        context['salary_list'] = salary_list
        context['year_list'] = year_list

        context['month'] = month
        context['name'] = name
        context['search_type'] = self.request.GET.get('type')
        return context
## 확인 필요
# month의 출근 퇴근 일반 요금 계산해서 Salary 생성
def new_salary(creator, month, member):
    last_date = datetime.strftime(datetime.strptime(month+'-01', FORMAT) + relativedelta(months=1) - timedelta(days=1), FORMAT)
    # attendance = DispatchRegularlyConnect.objects.filter(work_type='출근').filter(driver_id=member).filter(departure_date__range=(month+'-01 00:00', last_date+' 24:00')).aggregate(Sum('driver_allowance'))
    # leave = DispatchRegularlyConnect.objects.filter(work_type='퇴근').filter(driver_id=member).filter(departure_date__range=(month+'-01 00:00', last_date+' 24:00')).aggregate(Sum('driver_allowance'))
    # order = DispatchOrderConnect.objects.filter(driver_id=member).filter(departure_date__range=(month+'-01 00:00', last_date+' 24:00')).aggregate(Sum('driver_allowance'))

    # attendance_price = 0
    # leave_price = 0
    # order_price = 0
    # assignment_price = 0
    # regularly_assignment_price = 0

    base = 0
    service_allowance = 0
    performance_allowance = 0
    annual_allowance = 0
    overtime_allowance = 0
    meal = 0
    

    if TODAY[:7] <= month:
        base = int(member.base)
        service_allowance = int(member.service_allowance)
        performance_allowance = int(member.performance_allowance)
        annual_allowance = int(member.annual_allowance)
        overtime_allowance = int(member.overtime_allowance)
        meal = int(member.meal)

    # if salary:
    #     base = salary.base
    #     service_allowance = salary.service_allowance
    #     performance_allowance = salary.performance_allowance

    # Salary가 없을 때만 동작하는 함수라서 계산할 필요 없음
    # if attendance['driver_allowance__sum']:
    #     attendance_price = int(attendance['driver_allowance__sum'])
    # if leave['driver_allowance__sum']:
    #     leave_price = int(leave['driver_allowance__sum'])
    # if order['driver_allowance__sum']:
    #     order_price = int(order['driver_allowance__sum'])
    
    try:
        payment_date = Category.objects.get(type='급여지급일').category
    except:
        payment_date = 1


    salary = Salary(
        member_id = member,
        base = base,
        service_allowance = service_allowance,
        performance_allowance = performance_allowance,
        annual_allowance = annual_allowance,
        overtime_allowance = overtime_allowance,
        meal = meal,
        # attendance = attendance_price,
        # leave = leave_price,
        # order = order_price,
        # assignment = assignment_price,
        # regularly_assignment = regularly_assignment_price,
        attendance = 0,
        leave = 0,
        order = 0,
        assignment = 0,
        regularly_assignment = 0,
        total = 0,
        month = month,
        payment_date = payment_date,
        creator = creator
    )
    salary.save()
    salary.total = salary.calculate_total()
    return salary

def salary_detail(request):
    user_auth = request.session.get('authority')
    if user_auth >= 3:
        member_id_list = [request.session.get('user')]
    else:
        member_id_list = request.GET.get('driver').split(',')
    month = request.GET.get('date', TODAY[:7])
    
    # try:
    #     category_date = Category.objects.get(type='급여지급일').category
    #     if category_date == '말일':
    #         salary_date = datetime.strftime(datetime.strptime(month+'-01', FORMAT) + relativedelta(months=1) - timedelta(days=1), FORMAT)
    #     else:
    #         salary_date = f'{month}-{category_date}'
    # except Category.DoesNotExist:
    #     salary_date = ''
    
    member_list = []
    for member_id in member_id_list:
        member = get_object_or_404(Member, id=member_id)

        last_date = datetime.strftime(datetime.strptime(month+'-01', FORMAT) + relativedelta(months=1) - timedelta(days=1), FORMAT)[8:10]
        
        attendance_list = [''] * int(last_date)
        leave_list = [''] * int(last_date)
        order_list = [''] * int(last_date)
        assignment_list = [''] * int(last_date)
        regularly_assignment_list = [''] * int(last_date)

        order_price_list = [0] * int(last_date)
        attendance_price_list = [0] * int(last_date)
        leave_price_list = [0] * int(last_date)
        assignment_price_list = [0] * int(last_date)
        regularly_assignment_price_list = [0] * int(last_date)

        week_list = []

        order_cnt = 0
        attendance_cnt = 0
        leave_cnt = 0
        assignment_cnt = 0
        regularly_assignment_cnt = 0
        
        total_list = [0] * int(last_date)
        assignment_total_list = [0] * int(last_date)
        work_cnt = 0
        

        salary = Salary.objects.filter(member_id=member).get(month=month)
        meal = salary.meal
        payment_date = salary.payment_date
        if payment_date == '말일':
            salary_date = datetime.strftime(datetime.strptime(month+'-01', FORMAT) + relativedelta(months=1) - timedelta(days=1), FORMAT)
        else:
            salary_date = datetime.strftime(datetime.strptime(f'{month}-{payment_date}', FORMAT) - relativedelta(months=1), FORMAT)

        additional = salary.additional_salary.all()
        deduction = salary.deduction_salary.all()

        connects = DispatchOrderConnect.objects.filter(departure_date__range=(f'{month}-01 00:00', f'{month}-{last_date} 24:00')).filter(driver_id=member)
        order_cnt = connects.count()
        for connect in connects:
            c_date = int(connect.departure_date[8:10]) - 1
            if not order_list[c_date]:
                order_list[c_date] = []
            order_list[c_date].append([connect.order_id.departure, connect.order_id.arrival])
            
        # if connects:
            if connect.payment_method == 'n':
                order_price_list[c_date] += int(connect.driver_allowance)
                total_list[c_date] += int(connect.driver_allowance)

        attendances = DispatchRegularlyConnect.objects.filter(departure_date__range=(f'{month}-01 00:00', f'{month}-{last_date} 24:00')).filter(work_type='출근').filter(driver_id=member)
        attendance_cnt = attendances.count()
        for attendance in list(attendances.values('regularly_id__route', 'departure_date', 'driver_allowance')):
            c_date = int(attendance['departure_date'][8:10]) - 1
            if not attendance_list[c_date]:
                attendance_list[c_date] = []
            attendance_list[c_date].append(attendance['regularly_id__route'])

            attendance_price_list[c_date] += int(attendance['driver_allowance'])
        # if attendances:
            total_list[c_date] += int(attendance['driver_allowance'])

        leaves = DispatchRegularlyConnect.objects.filter(departure_date__range=(f'{month}-01 00:00', f'{month}-{last_date} 24:00')).filter(work_type='퇴근').filter(driver_id=member)
        leave_cnt = leaves.count()
        for leave in list(leaves.values('regularly_id__route', 'departure_date', 'driver_allowance')):
            c_date = int(leave['departure_date'][8:10]) - 1
            if not leave_list[c_date]:
                leave_list[c_date] = []
            leave_list[c_date].append(leave['regularly_id__route'])
        
            leave_price_list[c_date] += int(leave['driver_allowance'])
        # if leaves:
            total_list[c_date] += int(leave['driver_allowance'])

        # 업무 급여 데이터
        assignments = AssignmentConnect.objects.filter(start_date__range=(f'{month}-01 00:00', f'{month}-{last_date} 24:00')).filter(type='일반업무').filter(member_id=member)
        assignment_cnt = assignments.count()
        for assignment in list(assignments.values('assignment_id__assignment', 'start_date', 'allowance')):
            c_date = int(assignment['start_date'][8:10]) - 1
            if not assignment_list[c_date]:
                assignment_list[c_date] = []
            assignment_list[c_date].append(assignment['assignment_id__assignment'])

            assignment_price_list[c_date] += int(assignment['allowance'])
        # if assignments:
            assignment_total_list[c_date] += int(assignment['allowance'])
        
        regularly_assignments = AssignmentConnect.objects.filter(start_date__range=(f'{month}-01 00:00', f'{month}-{last_date} 24:00')).filter(type='고정업무').filter(member_id=member)
        regularly_assignment_cnt = regularly_assignments.count()
        for regularly_assignment in list(regularly_assignments.values('assignment_id__assignment', 'start_date', 'allowance')):
            c_date = int(regularly_assignment['start_date'][8:10]) - 1
            if not regularly_assignment_list[c_date]:
                regularly_assignment_list[c_date] = []
            regularly_assignment_list[c_date].append(regularly_assignment['assignment_id__assignment'])

            regularly_assignment_price_list[c_date] += int(regularly_assignment['allowance'])
        # if regularly_assignments:
            assignment_total_list[c_date] += int(regularly_assignment['allowance'])


        for i in range(int(last_date)):
            check = 0

            if i + 1 < 10:
                date = f'{month}-0{i+1}'
            else:
                date = f'{month}-{i+1}'

            week_list.append(WEEK[datetime.strptime(date, FORMAT).weekday()])

            if check == 1:
                work_cnt += 1

        total_cnt = leave_cnt + attendance_cnt + order_cnt
        assignment_total_cnt = assignment_cnt + regularly_assignment_cnt
        member_list.append({
            'order_list': order_list,
            'attendance_list': attendance_list,
            'leave_list': leave_list,
            'assignment_list': assignment_list,
            'regularly_assignment_list': regularly_assignment_list,
            'order_cnt': order_cnt,
            'total_cnt': total_cnt,
            'assignment_total_cnt': assignment_total_cnt,
            'attendance_cnt': attendance_cnt,
            'leave_cnt': leave_cnt,
            'assignment_cnt': assignment_cnt,
            'regularly_assignment_cnt': regularly_assignment_cnt,
            'order_price_list': order_price_list,
            'attendance_price_list': attendance_price_list,
            'leave_price_list': leave_price_list,
            'assignment_price_list': assignment_price_list,
            'regularly_assignment_price_list': regularly_assignment_price_list,
            'salary': salary,
            'member': member,
            'week_list': week_list,
            'total_list': total_list,
            'assignment_total_list': assignment_total_list,
            'work_cnt': work_cnt,
            'additional': additional,
            'deduction': deduction,
            'meal': meal,
            'salary_date': salary_date,
        })
        
    context = {
        'member_list': member_list,
        'month': month
    }
    return render(request, 'HR/salary_detail.html', context)

class ChangeSalaryList(SalaryList):
    template_name = 'HR/salary_change.html'
    context_object_name = 'member_list'
    model = Member

class OutsourcingSalaryList(SalaryList):
    template_name = 'HR/salary_outsourcing.html'
    context_object_name = 'member_list'
    model = Member  

class ManagerSalaryList(SalaryList):
    template_name = 'HR/salary_manager.html'
    context_object_name = 'member_list'
    model = Member  

def salary_edit(request):
    if request.method == 'POST':
        user_auth = request.session.get('authority')
        if user_auth >= 3:
            return render(request, 'authority.html')

        base_list = request.POST.getlist('base')
        service_list = request.POST.getlist('service')
        performance_list = request.POST.getlist('performance')
        annual_list = request.POST.getlist('annual')
        meal_list = request.POST.getlist('meal')
        id_list = request.POST.getlist('id')
        month = request.POST.get('month')

        for base, service, performance, annual, meal, id in zip(base_list, service_list, performance_list, annual_list, meal_list, id_list):
            member = get_object_or_404(Member, id=id)
            base = int(base.replace(',',''))
            service = int(service.replace(',',''))
            performance = int(performance.replace(',',''))
            annual = int(annual.replace(',',''))
            meal = int(str(meal).replace(',',''))

            salary = Salary.objects.filter(member_id=member).get(month=month)
            salary.base = base
            salary.service_allowance = service
            salary.performance_allowance = performance
            salary.annual_allowance = annual
            salary.meal = meal
            salary.save()
            salary.total = salary.calculate_total()
            salary.save()

            if TODAY[:7] <= month:
                member.base = base
                member.service_allowance = service
                member.performance_allowance = performance
                member.annual_allowance = annual
                member.save()

                # 선택한 달 이후 급여들 다 업데이트
                # edit_salary_list = Salary.objects.filter(month__gt=month).filter(member_id=member)
                # for e_salary in edit_salary_list:
                #     e_salary.base = base
                #     e_salary.service_allowance = service
                #     e_salary.performance_allowance = performance
                #     e_salary.total = int(e_salary.meal) + int(e_salary.attendance) + int(e_salary.leave) + int(e_salary.order) + int(e_salary.base) + int(e_salary.service_allowance) + int(e_salary.performance_allowance) + int(e_salary.additional) - int(e_salary.deduction)
                #     e_salary.save()



        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def salary_change_edit(request):
    if request.method == 'POST':
        user_auth = request.session.get('authority')
        if user_auth >= 3:
            return render(request, 'authority.html')

        overtime_list = request.POST.getlist('overtime')
        performance_list = request.POST.getlist('performance')
        id_list = request.POST.getlist('id')
        month = request.POST.get('month')

        for overtime, performance, id in zip(overtime_list, performance_list, id_list):
            member = get_object_or_404(Member, id=id)
            overtime = int(overtime.replace(',',''))
            performance = int(performance.replace(',',''))

            salary = Salary.objects.filter(member_id=member).get(month=month)
            salary.overtime_allowance = overtime
            salary.performance_allowance = performance
            salary.save()
            salary.total = salary.calculate_total()
            salary.save()

            if TODAY[:7] <= month:
                member.overtime_allowance = overtime
                member.performance_allowance = performance
                member.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def salary_outsourcing_edit(request):
    if request.method == 'POST':
        user_auth = request.session.get('authority')
        if user_auth >= 3:
            return render(request, 'authority.html')

        performance_list = request.POST.getlist('performance')
        id_list = request.POST.getlist('id')
        month = request.POST.get('month')

        for performance, id in zip(performance_list, id_list):
            member = get_object_or_404(Member, id=id)
            performance = int(performance.replace(',',''))

            salary = Salary.objects.filter(member_id=member).get(month=month)
            salary.performance_allowance = performance
            salary.save()
            salary.total = salary.calculate_total()
            salary.save()

            if TODAY[:7] <= month:
                member.performance_allowance = performance
                member.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def salary_manager_edit(request):
    if request.method == 'POST':
        user_auth = request.session.get('authority')
        if user_auth >= 3:
            return render(request, 'authority.html')

        performance_list = request.POST.getlist('performance')
        id_list = request.POST.getlist('id')
        month = request.POST.get('month')

        for performance, id in zip(performance_list, id_list):
            member = get_object_or_404(Member, id=id)
            performance = int(performance.replace(',',''))

            salary = Salary.objects.filter(member_id=member).get(month=month)
            salary.performance_allowance = performance
            salary.save()
            salary.total = salary.calculate_total()
            salary.save()

            if TODAY[:7] <= month:
                member.performance_allowance = performance
                member.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def salary_additional_create(request):
    if request.method == 'POST':
        user_auth = request.session.get('authority')
        if user_auth >= 3:
            return render(request, 'authority.html')

        member_id = request.POST.get('id', '')
        price = request.POST.get('price', '0').replace(',','')
        if price == '':
            price = '0'
        remark = request.POST.get('remark')
        month = request.POST.get('month')
        creator = Member.objects.get(pk=request.session.get('user'))

        member = get_object_or_404(Member, id=member_id)
        salary = Salary.objects.filter(member_id=member).get(month=month)

        additional = AdditionalSalary(
            salary_id = salary,
            member_id = member,
            price = price,
            remark = remark,
            creator = creator,
        )
        additional.save()
        salary.additional = int(salary.additional) + int(price)
        salary.total = int(salary.total) + int(price)
        salary.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def salary_additional_delete(request):
    if request.method == 'POST':
        user_auth = request.session.get('authority')
        if user_auth >= 3:
            return render(request, 'authority.html')

        id_list = request.POST.getlist('id')
        for id in id_list:
            additional = get_object_or_404(AdditionalSalary, id=id)
            
            salary = additional.salary_id
            salary.additional = int(salary.additional) - int(additional.price)
            salary.total = int(salary.total) - int(additional.price)
            salary.save()
            
            additional.delete()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])


def salary_deduction_create(request):
    if request.method == 'POST':
        user_auth = request.session.get('authority')
        if user_auth >= 3:
            return render(request, 'authority.html')

        member_id = request.POST.get('id', '')
        price = request.POST.get('price', '0').replace(',','')
        if price == '':
            price = '0'
        remark = request.POST.get('remark')
        month = request.POST.get('month')
        creator = Member.objects.get(pk=request.session.get('user'))

        member = get_object_or_404(Member, id=member_id)
        salary = Salary.objects.filter(member_id=member).get(month=month)

        deduction = DeductionSalary(
            salary_id = salary,
            member_id = member,
            price = price,
            remark = remark,
            creator = creator,
        )
        deduction.save()
        salary.deduction = int(salary.deduction) + int(price)
        salary.total = int(salary.total) - int(price)
        salary.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def salary_deduction_delete(request):
    if request.method == 'POST':
        user_auth = request.session.get('authority')
        if user_auth >= 3:
            return render(request, 'authority.html')

        id_list = request.POST.getlist('id')
        for id in id_list:
            deduction = get_object_or_404(DeductionSalary, id=id)
            
            salary = deduction.salary_id
            salary.deduction = int(salary.deduction) - int(deduction.price)
            salary.total = int(salary.total) + int(deduction.price)
            salary.save()
            
            deduction.delete()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])


def salary_load(request):
    if request.method == 'POST':
        user_auth = request.session.get('authority')
        if user_auth >= 3:
            return render(request, 'authority.html')

        id_list = request.POST.getlist('member_id')
        month = request.POST.get('month')
        prev_month = datetime.strftime(datetime.strptime(f'{month}-01', FORMAT) - relativedelta(months=1), FORMAT)[:7]

        for id in id_list:
            member = get_object_or_404(Member, id=id)
            try:
                prev_salary = Salary.objects.filter(month=prev_month).get(member_id=member)
            except Salary.DoesNotExist:
                continue
            base = prev_salary.base
            service_allowance = prev_salary.service_allowance
            performance_allowance = prev_salary.performance_allowance
            annual_allowance = prev_salary.annual_allowance
            overtime_allowance = prev_salary.overtime_allowance
            meal = prev_salary.meal

            salary = Salary.objects.filter(month=month).get(member_id=member)
            salary.base = base
            salary.service_allowance = service_allowance
            salary.performance_allowance = performance_allowance
            salary.annual_allowance = annual_allowance
            salary.overtime_allowance = overtime_allowance
            salary.meal = meal
            salary.total = salary.calculate_total()
            # salary.total = int(salary.meal) + int(salary.attendance) + int(salary.leave) + int(salary.order) + int(salary.base) + int(salary.service_allowance) + int(salary.performance_allowance) + int(salary.annual_allowance) + int(salary.additional) - int(salary.deduction)
            salary.save()
            

        
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])