# Generated by Django 4.0.5 on 2024-08-14 15:33

import approval.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('humanresource', '0009_salary_new_annual_allowance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_type', models.CharField(max_length=100, verbose_name='결제 종류')),
                ('title', models.CharField(max_length=100, verbose_name='결제 종류')),
                ('content', models.TextField(verbose_name='내용')),
                ('status', models.CharField(max_length=100, verbose_name='현황')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='작성시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정시간')),
                ('creator', models.ForeignKey(db_column='creator_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approval_creator', to='humanresource.member')),
                ('next_approver_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_approver', to='humanresource.member')),
            ],
        ),
        migrations.CreateModel(
            name='Approver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, verbose_name='내용')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='작성시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정시간')),
                ('approval_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approver', to='approval.approval')),
                ('creator', models.ForeignKey(db_column='creator_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approver_creator', to='humanresource.member')),
            ],
        ),
        migrations.CreateModel(
            name='ApprovalFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=approval.models.ApprovalFile.get_file_path)),
                ('filename', models.TextField(null=True, verbose_name='첨부파일명')),
                ('path', models.TextField(null=True, verbose_name='경로')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='작성시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정시간')),
                ('creator', models.ForeignKey(db_column='user_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approval_file_user', to='humanresource.member')),
                ('member_id', models.ForeignKey(db_column='approval_id', on_delete=django.db.models.deletion.CASCADE, related_name='approval_file', to='humanresource.member')),
            ],
        ),
    ]