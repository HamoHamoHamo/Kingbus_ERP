# Generated by Django 3.1.5 on 2021-04-22 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dispatch', '0001_initial'),
        ('crudmember', '0001_initial'),
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailysalary',
            name='connect_id',
            field=models.ForeignKey(blank=True, db_column='connect_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='salary_daily_connect', to='dispatch.dispatchconnect'),
        ),
        migrations.AddField(
            model_name='dailysalary',
            name='creator',
            field=models.ForeignKey(db_column='user_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='salary_daily_user', to='crudmember.user'),
        ),
        migrations.AddField(
            model_name='dailysalary',
            name='monthly_salary',
            field=models.ForeignKey(db_column='monthly_id', on_delete=django.db.models.deletion.CASCADE, related_name='salary_daily', to='accounting.monthlysalary'),
        ),
        migrations.AddField(
            model_name='collect',
            name='connect_id',
            field=models.ForeignKey(db_column='connect_id', on_delete=django.db.models.deletion.CASCADE, related_name='collect_connect', to='dispatch.dispatchconnect'),
        ),
        migrations.AddField(
            model_name='collect',
            name='creator',
            field=models.ForeignKey(db_column='user_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collect_user', to='crudmember.user'),
        ),
    ]