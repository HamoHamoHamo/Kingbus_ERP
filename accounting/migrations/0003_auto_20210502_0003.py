# Generated by Django 3.1.5 on 2021-05-02 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_auto_20210422_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlysalary',
            name='payment_month',
            field=models.CharField(default='2021-05', max_length=7, verbose_name='지급월'),
        ),
    ]