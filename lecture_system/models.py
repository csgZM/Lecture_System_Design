from django.db import models


# Create your models here.
class Lecture_Message(models.Model):
    Lecture_title = models.CharField(max_length=100, verbose_name='讲座标题')
    Lecture_Pname = models.CharField(max_length=100, verbose_name='主讲人')
    Lecture_introdution = models.CharField(max_length=300, verbose_name='讲座内容介绍')
    Lecture_SN = models.CharField(max_length=10, verbose_name='讲座最大预约人数')
    Lecture_category = models.CharField(max_length=20, verbose_name='讲座类型标签')
    Lecture_Stime = models.CharField(max_length=20, verbose_name='讲座开始时间')
    Lecture_Etime = models.CharField(max_length=20, verbose_name='讲座结束时间')
    Lecture_Location = models.CharField(max_length=50, verbose_name='讲座地点')

    class Meta:
        verbose_name_plural = '讲座信息表'  # 修改管理级页面显示
