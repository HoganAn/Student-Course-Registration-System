# Generated by Django 3.2.2 on 2021-06-02 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20210524_1427'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name_plural': '学生'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'verbose_name_plural': '教师'},
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('male', '男'), ('female', '女')], default='男', max_length=10, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='gender',
            field=models.CharField(choices=[('male', '男'), ('female', '女')], default='男', max_length=10, verbose_name='性别'),
        ),
    ]
