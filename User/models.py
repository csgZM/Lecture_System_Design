from django.db import models


# Create your models here.
class GetPublish(models.Model):
    username = models.CharField(max_length=30, verbose_name='用户名')
    reason = models.CharField(max_length=200, verbose_name='申请理由')
    apply_time = models.CharField(max_length=30, verbose_name='申请时间')

    class Meta:
        verbose_name_plural = '讲座发布权限申请表'  # 修改管理级页面显示


class sign_publish(models.Model):
    l_id = models.CharField(max_length=10, verbose_name='讲座id')
    signPassword = models.CharField(max_length=30, verbose_name='签到密码')
    p_id = models.CharField(max_length=20, verbose_name='发布人用户名')

    class Meta:
        verbose_name_plural = '讲座对应签到表'  # 修改管理级页面显示


class lecture_experience(models.Model):
    user_id = models.CharField(max_length=20, verbose_name='用户名')
    l_id = models.CharField(max_length=10, verbose_name='讲座id')
    title = models.CharField(max_length=200, verbose_name='讲座心得标题')
    content = models.CharField(max_length=2000, verbose_name='讲座心得内容')

    class Meta:
        verbose_name_plural = '讲座心得记录表'  # 修改管理级页面显示
