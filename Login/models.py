from django.db import models
import django.utils.timezone as timezone


# Create your models here

class Register_UserInfo(models.Model):  # 注册页面信息的数据库操作
    Username = models.CharField(max_length=20, verbose_name='用户名', primary_key=True)
    PassWord = models.CharField(max_length=20, verbose_name='用户密码')
    PhoneNumber = models.CharField(max_length=15, verbose_name='用户电话')
    Email = models.CharField(max_length=20, verbose_name='用户邮件')
    nikename = models.CharField(max_length=30, verbose_name='用户昵称')

    class Meta:
        verbose_name_plural = '用户信息表'  # 修改管理级页面显示


class UserToken(models.Model):
    token = models.CharField(max_length=60, verbose_name='用户token')
    publish_power = models.CharField(max_length=10, verbose_name='发布权限')
    user_id = models.OneToOneField('Register_UserInfo', on_delete=models.CASCADE, verbose_name='用户id')

    class Meta:
        verbose_name_plural = '用户发布权限表'  # 修改管理级页面显示


class Reserved_Lecture(models.Model):  # 讲座预约表
    maxNum = models.CharField(max_length=10, verbose_name='最大预约人数')
    reservedNum = models.CharField(max_length=10, verbose_name='已预约人数')
    user_id = models.CharField(max_length=50, verbose_name='用户id')
    lecture_id = models.CharField(max_length=20, verbose_name="讲座id")

    # lecture_id = models.ManyToManyField('Lecture_Message',verbose_name='讲座id')
    class Meta:
        verbose_name_plural = '讲座预约记录表'  # 修改管理级页面显示


class Listened_Lecture(models.Model):  # 讲座记录表
    user_id = models.CharField(max_length=50, verbose_name='用户id')
    lecture_id = models.CharField(max_length=20, verbose_name="讲座id")

    class Meta:
        verbose_name_plural = '讲座已参加记录表'  # 修改管理级页面显示


class Published_Lecture(models.Model):  # 讲座发布记录表
    user_id = models.ForeignKey("UserToken", on_delete=models.CASCADE)
    lecture_id = models.CharField(max_length=20, verbose_name="讲座id")

    class Meta:
        verbose_name_plural = '讲座发布记录表'  # 修改管理级页面显示


class Teacher_indentity(models.Model):  # 验证管理员注册的用户名必须为老师职公号（开启校园认证后，启用该表）
    Teacher_id = models.CharField(max_length=40, verbose_name='老师职工号')


class Stuedent_indentity(models.Model):  # 学生注册时的用户名必须为学生学号（开启校园认证后，启用该表）
    Student_id = models.CharField(max_length=40, verbose_name='学生学号')
