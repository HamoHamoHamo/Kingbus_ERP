from django.contrib import admin
from .models import Outlay, Income, Salary, Collect



admin.site.register(Outlay)
admin.site.register(Salary)
admin.site.register(Income)
admin.site.register(Collect)