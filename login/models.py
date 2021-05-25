from django.db import models


# Create your models here.


class Person(models.Model):
    sex = (
        ('male', "男"),
        ('female', "女"),
    )

    name = models.CharField(max_length=10, verbose_name="姓名")
    gender = models.CharField(max_length=10, choices=sex, default="男")
    faculty = models.CharField(max_length=20, verbose_name="学院")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    password = models.CharField(max_length=32, verbose_name="密码")
    info = models.CharField(max_length=255, verbose_name="个人简介", help_text="一句话介绍自己，不要超过250字", default="本人很懒，没有设置个人简介")

    class Meta:
        abstract = True


class Student(Person):
    uid = models.CharField(max_length=12, verbose_name="学号", unique=True)
    grade = models.CharField(max_length=5, verbose_name="年级")

    def __str__(self):
        return self.name


class Teacher(Person):
    uid = models.CharField(max_length=12, verbose_name="教工号", unique=True)

    def __str__(self):
        return self.name
