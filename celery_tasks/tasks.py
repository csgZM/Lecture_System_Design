#使用celery
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django.settings')
django.setup()
#创建Celery类的实例对象
app=Celery('celery_tasks.tasks',broker='redis://:12345@127.0.0.1:6379/8')
#开启celery命令（celery -A celery_tasks.tasks  worker -l info -P eventlet）
#定义任务函数
@app.task
def send_lisener_inlecture_email(to_emal,l_id,token):
    sender = settings.DEFAULT_FROM_EMAIL
    print(to_emal)
    res = send_mail(  # 发送请求地址http://127.0.0.1:8000/.......
        '讲座管理系统-签到模块',
        f'点击此处进入签到界面',
        sender,
        [to_emal],
        html_message='<h1>欢迎来到签到页面</h1>请点击下面链接进行签到<a>http://127.0.0.1:8000/lecture_index/sign/%s/%s</a>' % (l_id, token)
    )
    print('211')
    print('res=', res)