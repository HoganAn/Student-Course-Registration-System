from django.db import models

# Create your models here.
import login.models


class Prerequisite(models.Model):
    pre_course_id = models.CharField(max_length=15, verbose_name='先修课程代码')


class Course(models.Model):
    course_name = models.CharField(max_length=50, verbose_name='课程名称')
    course_id = models.CharField(max_length=15, verbose_name='课程代码', unique=True)
    duration = models.IntegerField(verbose_name='上课时间')
    capacity = models.IntegerField(verbose_name='课程容量')
    faculty = models.CharField(max_length=20, verbose_name="开课学院")
    info = models.CharField(max_length=255, verbose_name="课程介绍", blank=True, default="暂无课程介绍")
    lecturer_uid = models.ForeignKey(login.models.Teacher, on_delete=models.CASCADE, verbose_name="授课教师教工号")
    prerequisite = models.ManyToManyField(Prerequisite, blank=True)
    reg_stat = models.ManyToManyField(login.models.Student, through='CourseRegistration')


class CourseRegistration(models.Model):
    stu = models.ForeignKey(login.models.Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_joined = models.CharField(max_length=1, verbose_name="选课状态", default='0')
