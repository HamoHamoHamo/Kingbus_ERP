# Generated by Django 3.1.5 on 2021-02-13 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humanresource', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hr',
            name='date',
            field=models.DateTimeField(verbose_name='날짜'),
        ),
        migrations.AlterField(
            model_name='hr',
            name='pub_date',
            field=models.DateTimeField(verbose_name='등록날짜'),
        ),
    ]