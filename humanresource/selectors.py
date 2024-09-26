from django.db.models import Q

from .models import Member, Salary

class MemberSelector:
    def get_using_driver_list(self, name):
        member = Member.objects.filter(use='사용').filter(Q(role='팀장')|Q(role='운전원')|Q(role='용역')).order_by('name')
        if name:
            member = member.filter(name__startswith=name)
        return member

    # 정규직
    def get_using_permanent_driver_list(self, name):
        member = Member.objects.filter(use='사용').filter(Q(role='팀장')|Q(role='운전원')).order_by('name')
        if name:
            member = member.filter(name__startswith=name)
        return member

    # 용역
    def get_using_outsourcing_driver_list(self, name):
        member = Member.objects.filter(use='사용').filter(role='용역').order_by('name')
        if name:
            member = member.filter(name__startswith=name)
        return member

    def get_monthly_salary_list(self, month):
        return list(Salary.objects.filter(month=month, member_id__use='사용').values(
            'member_id',
            'base',
            'service_allowance',
            'performance_allowance',
            'annual_allowance',
            'overtime_allowance',
            'meal',
            'attendance',
            'leave',
            'order',
            'additional',
            'deduction',
            'weekly_holiday_allowance_deduction',
            'assignment',
            'regularly_assignment',
            'total',
            'month',
            'payment_date',

            'new_annual_allowance',
            'team_leader_allowance_roll_call',
            'team_leader_allowance_vehicle_management',
            'team_leader_allowance_task_management',
            'full_attendance_allowance',
            'diligence_allowance',
            'accident_free_allowance',
            'welfare_meal_allowance',
            'welfare_fuel_allowance',
        ))