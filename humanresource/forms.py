from django import forms 
from django.db import models

from .models import Member, Salary

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'name',
            'role',
            'birthdate',
            'address',
            'phone_num',
            'entering_date',
            'note',
            'interview_date',
            'contract_date',
            'contract_renewal_date',
            'contract_condition',
            'renewal_reason',
            'apply_path',
            'career',
            'position',
            'apprenticeship_note',
            'leave_reason',
            'resident_number1',
            'resident_number2',
            #'company',
            #'team',
            'final_opinion',
            'interviewer',
            'end_date',
            'leave_date',
            'allowance_type',
            'license',
        ]

# class HRForm(forms.ModelForm):
#     class Meta:
#         model = HR
#         fields = [
#             'hr_type',
#             'reason',
#             'start_date',
#             'end_date',
#         ]

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = [
            'service_allowance',
            # 'new_annual_allowance',
            'team_leader_allowance_roll_call',
            'team_leader_allowance_vehicle_management',
            'team_leader_allowance_task_management',
            'full_attendance_allowance',
            'diligence_allowance',
            'accident_free_allowance',
            # 'welfare_meal_allowance',
            'welfare_fuel_allowance',
        ]