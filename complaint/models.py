from datetime import datetime
from django.db import models
from humanresource.models import Member
from uuid import uuid4
from vehicle.models import Vehicle

class Consulting(models.Model):
    member_id = models.ForeignKey(Member, verbose_name='신청인', related_name="consulting", on_delete=models.CASCADE, null=True)
    content = models.TextField(verbose_name='상담사유', null=False)
    date = models.CharField(verbose_name='신청일', max_length=16, null=False, blank=True)
    check_member_id = models.ForeignKey(Member, verbose_name='확인한 직원', related_name="consulting_check", on_delete=models.SET_NULL, null=True)
    status = models.CharField(verbose_name='처리상태', max_length=50, null=False, default="처리전")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="consulting_crator", db_column="creator_id", null=True)

class ConsultingFile(models.Model):
    def get_file_path(instance, filename):
        
        ymd_path = datetime.now().strftime('%Y/%m/%d')
        uuid_name = uuid4().hex
        return '/'.join(['complaint/consulting', ymd_path, uuid_name])

    consulting_id = models.ForeignKey(Consulting, on_delete=models.CASCADE, related_name="consulting_file", db_column="consulting_id", null=True)
    file = models.FileField(upload_to=get_file_path, blank=True, null=True)
    filename = models.CharField(max_length=1024, null=True, verbose_name='첨부파일명')

    def __str__(self):
        return f'{self.consulting_id.member_id.name} {str(self.consulting_id.pub_date)[:16]}'

class VehicleInspectionRequest(models.Model):
    member_id = models.ForeignKey(Member, verbose_name='신청인', related_name="inspection_request_application", on_delete=models.SET_NULL, null=True)
    vehicle_id = models.ForeignKey(Vehicle, verbose_name='차량', related_name="inspection_request_application", on_delete=models.SET_NULL, null=True)
    content = models.TextField(verbose_name='신청내용', null=False)
    date = models.CharField(verbose_name='신청일', max_length=16, null=False)
    check_member_id = models.ForeignKey(Member, verbose_name='확인한 직원', related_name="inspection_request_application_check", on_delete=models.SET_NULL, null=True)
    status = models.CharField(verbose_name='처리상태', max_length=50, null=False, default="처리전")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    creator = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="inspection_request_application_creator", db_column="creator_id", null=True)

class InspectionRequestFile(models.Model):
    def get_file_path(instance, filename):
        
        ymd_path = datetime.now().strftime('%Y/%m/%d')
        uuid_name = uuid4().hex
        return '/'.join(['complaint/inspection', ymd_path, uuid_name])

    inspection_request_id = models.ForeignKey(VehicleInspectionRequest, on_delete=models.CASCADE, related_name="inspection_request_file", db_column="inspection_request_id", null=True)
    file = models.FileField(upload_to=get_file_path, blank=True, null=True)
    filename = models.CharField(max_length=1024, null=True, verbose_name='첨부파일명')

    def __str__(self):
        return f'{self.inspection_request_id.member_id.name} {str(self.inspection_request_id.pub_date)[:16]}'