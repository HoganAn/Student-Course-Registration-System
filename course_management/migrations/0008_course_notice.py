# Generated by Django 3.2.2 on 2021-06-08 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_management', '0007_auto_20210602_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='notice',
            field=models.CharField(default='暂无课程通知', max_length=1000, verbose_name='课程通知'),
        ),
    ]
