# Generated by Django 3.1.5 on 2021-04-26 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0002_dispatchconnect_bus_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispatchconsumer',
            name='company',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='거래처'),
        ),
        migrations.AddField(
            model_name='dispatchorder',
            name='routine',
            field=models.BooleanField(default=False, verbose_name='정기배차'),
        ),
    ]