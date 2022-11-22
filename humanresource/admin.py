from django.contrib import admin
from .models import Member, MemberFile, Salary, AdditionalSalary, DeductionSalary


admin.site.register(Member)
admin.site.register(MemberFile)
admin.site.register(Salary)
admin.site.register(AdditionalSalary)
admin.site.register(DeductionSalary)