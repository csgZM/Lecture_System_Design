from django.shortcuts import render
from django.shortcuts import render, HttpResponse, reverse, redirect
from .models import Register_UserInfo, UserToken, Teacher_indentity
from django.views.generic import View
import json
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


# Create your views here.


class FirstView(View):  # 登录视图
    def get(self, request):
        checked = ''
        username = request.COOKIES.get('username')
        if 'password' in request.COOKIES:
            password = request.COOKIES.get('password')
            checked = 'checked'
        else:
            password = ''
        return render(request, 'login.html', {'username': username, 'password': password, 'checked': checked,
                                              'message': json.dumps(
                                                  '1')})  # 返回message是为了防止前端报错，其值为‘1’防止通过这个get方法得到登录页面时而出现密码或账号错误的提示弹窗！

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        token = username
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                UserToken.objects.update_or_create(
                    user_id=Register_UserInfo.objects.filter(Username=username, PassWord=password).first()
                    , defaults={'token': token}
                )
                if user.is_superuser:
                    return redirect('http://127.0.0.1:8000/admin')
                else:
                    response = redirect('lecture_system:index')
                    response.set_cookie('username', username, expires=datetime.now() + timedelta(days=14))
                    if remember == 'on':
                        response.set_cookie('password', password, expires=datetime.now() + timedelta(days=14))
                        return response
                    else:
                        response.delete_cookie('password')
                        return response
            else:
                return render(request, 'login.html', {'message': json.dumps("该账号已停用")})
        else:
            if User.objects.filter(username=username):
                return render(request, 'login.html', {'message': json.dumps("密码错误")})
            else:
                return render(request, 'login.html', {'message': json.dumps("用户名不存在")})


class RegistView(View):
    def get(self, request):
        return render(request, 'registered.html',
                      {'message': json.dumps('1')})  # 返回message是为了防止前端报错，其值为‘1’防止通过这个get方法得到注册页面时出现管理员注册时的错误信息

    def post(self, request):
        nikename = 'nikename' + '_' + request.POST['username']
        print(request.POST['identity'])
        if request.POST['identity'] == 'is_superuser':
            if Teacher_indentity.objects.filter(Teacher_id=request.POST.get('username')):
                user = Register_UserInfo(Username=request.POST['username'], PassWord=request.POST['password'],
                                         PhoneNumber=request.POST['phonenumber'], Email=request.POST['email'],
                                         nikename=nikename)
                user.save()
                R = User.objects.create_user(username=request.POST['username'], password=request.POST['password'],
                                             last_name=request.POST['phonenumber'], email=request.POST['email'],
                                             is_superuser='True', is_staff='True')
                R.save()
                print('123')
                return render(request, 'regist_success.html')
            else:
                return render(request, 'registered.html', {'message': json.dumps('教师职工号不存在或错误无法注册管理员账号')})
        else:
            user = Register_UserInfo(Username=request.POST['username'], PassWord=request.POST['password'],
                                     PhoneNumber=request.POST['phonenumber'], Email=request.POST['email'],
                                     nikename=nikename)
            user.save()
            R = User.objects.create_user(username=request.POST['username'], password=request.POST['password'],
                                         last_name=request.POST['phonenumber'], email=request.POST['email'])
            R.is_superuser = 0
            R.save()
            print('111')
            return render(request, 'regist_success.html')


def checkusername(request):  # 注册时，检验密码是否已存在,且对注册用户身份进行验证
    if request.method == "POST":
        username = request.POST.get('username')
        indentity = request.POST.get('indentity')
    if Register_UserInfo.objects.filter(Username=username):
        return HttpResponse(json.dumps(
            {
                'message': "该用户已存在"
            }
        ))
    else:
        return HttpResponse(json.dumps(
            {
                'message': ''
            }
        ))


def checkpassword(request):  # 注册时检验密码是否存在
    if request.method == "POST":
        password = request.POST.get('password')
    if Register_UserInfo.objects.filter(PassWord=password):
        return HttpResponse(json.dumps(
            {
                'message': "密码已存在"
            }
        ))
    else:
        return HttpResponse(json.dumps(
            {
                'message': ''
            }
        ))


def checkphonenumber(request):
    if request.method == "POST":
        phonenumber = request.POST.get('phonenumber')
    if Register_UserInfo.objects.filter(PhoneNumber=phonenumber):
        return HttpResponse(json.dumps(
            {
                'message': "该号码已被注册"
            }
        ))
    else:
        return HttpResponse(json.dumps(
            {
                'message': ''
            }
        ))


def checkemail(request):
    if request.method == "POST":
        email = request.POST.get('email')
    if Register_UserInfo.objects.filter(Email=email):
        return HttpResponse(json.dumps(
            {
                'message': "该邮箱已被注册"
            }
        ))
    else:
        return HttpResponse(json.dumps(
            {
                'message': ''
            }
        ))


class ReturnLoginView(View):
    def get(self, request):
        return redirect(reverse('Login:login'))


def regist_success(request):  # 控制注册成功后跳转的页面
    if request.method == "GET":
        return render(request, 'regist_success.html')
    else:
        return redirect(reverse('Login:login'))


def ajax_reserve(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        l_id = request.POST['l_id']
        print('用户id：%s  讲座id:%s', (user_id, l_id))
    return (json.dumps(
        {
            'message': 's '
        }))


class Forgetpassword(View):
    def get(self, requst):
        return render(requst, 'fpassword.html')

    def post(self, request):
        email = request.POST.get("email")
        c = Register_UserInfo.objects.get(Email=email)
        fpssword = c.PassWord
        fusername = c.Username
        sender = settings.DEFAULT_FROM_EMAIL
        res = send_mail(
            '讲座管理系统找回账号和密码',
            f'账号为：{fusername},密码为:{fpssword}',
            sender,
            [f'{email}'],
        )
        print('res=', res)
        return render(request, 'fpassword_success.html')


def check_bindemail(request):
    if request.method == "POST":
        email = request.POST.get('email')
    if Register_UserInfo.objects.filter(Email=email):
        return HttpResponse(json.dumps(
            {
                'message': ''
            }
        ))
    else:
        return HttpResponse(json.dumps(
            {
                'message': '该邮箱未注册'
            }
        ))
