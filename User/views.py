from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from Login.models import Register_UserInfo, Reserved_Lecture, Listened_Lecture, Published_Lecture, UserToken
from lecture_system.models import Lecture_Message
from django.views.generic import View
import json
from celery_tasks.tasks import send_lisener_inlecture_email
from django.conf import settings
from django.core.mail import send_mail
from .models import GetPublish, sign_publish, lecture_experience
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.contrib.auth import update_session_auth_hash


# Create your views here.


class IndexView(View):  # 用户个人界面视图
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        username = str(request.user)
        name = Register_UserInfo.objects.filter(Username=request.user).values()[0]["nikename"]
        p_lecture = []
        r_lecture = []
        l_lecture = []
        userMessage = Register_UserInfo.objects.filter(Username=username).first()

        U = UserToken.objects.filter(user_id=username).first()
        if U.published_lecture_set.all().values():
            for p_id in U.published_lecture_set.all().values():
                p_lecture.append(Lecture_Message.objects.filter(id=p_id['lecture_id']).values()[0])

        if Reserved_Lecture.objects.filter(user_id=username).values():
            for r_id in Reserved_Lecture.objects.filter(user_id=username).values():
                r_lecture.append(Lecture_Message.objects.filter(id=r_id['lecture_id']).values()[0])

        if Listened_Lecture.objects.filter(user_id=username).values():
            for l_id in Listened_Lecture.objects.filter(user_id=username).values():
                L = Lecture_Message.objects.filter(id=l_id['lecture_id']).values()[0]
                try:  # 找出已听讲座的讲座心得填写的情况
                    P = lecture_experience.objects.get(l_id=L['id'], user_id=username)
                    L['status'] = '已提交'
                except lecture_experience.DoesNotExist:
                    L['status'] = '未提交'
                l_lecture.append(L)
        return render(request, 'user_details.html', {'UserMessage': userMessage,
                                                     'plecture': p_lecture,
                                                     'rlecture': r_lecture,
                                                     'llecture': l_lecture,
                                                     'name': name,
                                                     })


class Lecture_ExperienceView(View):  # 填写讲座个人心得的视图
    @method_decorator(login_required)
    def get(self, request):
        username = request.user
        l_id = request.GET['l_id']
        print(l_id, username)
        try:
            P = lecture_experience.objects.get(l_id=l_id, user_id=username)
            return render(request, 'lecture_experience.html',
                          {
                              'title': json.dumps(P.title),
                              'content': json.dumps(P.content),
                              'result': json.dumps(1),
                              'Username': username,
                              'l_id': l_id
                          }
                          )
        except lecture_experience.DoesNotExist:
            return render(request, 'lecture_experience.html', {
                'result': json.dumps(0),
                'Username': username,
                'l_id': l_id
            }
                          )


def experience(request):
    username = request.user
    if request.method == 'POST':
        l_id = request.POST.get('l_id')
        title = request.POST.get('title')
        content = request.POST.get('content')
        print(username, l_id)
    try:
        P = lecture_experience.objects.get(l_id=l_id, user_id=username)
        P.title = title
        P.content = content
        P.save()
        print("修改")
        return HttpResponse(json.dumps(
            {
                'message': '修改成功'
            }
        )
        )
    except lecture_experience.DoesNotExist:
        lecture_experience.objects.update_or_create(
            user_id=username,
            l_id=l_id,
            title=title,
            content=content
        )
        print('提交')
        return HttpResponse(
            json.dumps(
                {
                    'message': '提交成功'
                }
            )
        )


def logout_view(request):
    logout(request)
    response = redirect('Login:login')
    # response.delete_cookie('')#删除相应的cookie
    return response


class RpasswordView(View):  # 修改密码视图
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'rpassword.html')

    def post(self, request):
        token = str(request.user)
        rpassword = request.POST.get('rpassword')
        try:
            R = Register_UserInfo.objects.get(Username=token)
            R.PassWord = rpassword
            R.save()
            u = User.objects.get(username=token)
            u.set_password(rpassword)
            u.save()
            return render(request, 'Rsuccess.html')
        except Exception:
            return HttpResponse("修改失败")


def checkrpassowrd(request):
    if request.method == "POST":
        Username = request.user
        password = request.POST.get("password")
        print(password)
        opassword = Register_UserInfo.objects.filter(Username=Username).values()[0]["PassWord"]
        if password == opassword:
            return HttpResponse(json.dumps({
                'message': "修改的密码不能和上一次的密码一样"
            }))
        if Register_UserInfo.objects.get(PassWord=password):
            return HttpResponse(json.dumps({
                'message': "该密码已被别人使用"
            }))

        return HttpResponse(json.dumps({
            'message': ""
        }))


def rname(request):
    if request.method == "POST":
        name = request.POST.get('name')
        try:
            U = Register_UserInfo.objects.get(Username=str(request.user))
            U.nikename = name
            U.save()
        except Exception:
            return HttpResponse(json.dumps({
                'result': '修改失败请重新再试'
            }))
        return HttpResponse(json.dumps({
            'result': '名字修改成功'
        }))
    else:
        return HttpResponse(json.dumps({
            'result': '修改失败请重新再试'
        }))


def getpublish(request):
    if request.method == "POST":
        reason = request.POST.get('reason')
        time = request.POST.get('time')
        username = str(request.user)
        try:
            GetPublish.objects.update_or_create(
                username=username,
                reason=reason,
                apply_time=time
            )
        except Exception:
            print(Exception)
            return HttpResponse(json.dumps({
                'result': '提交失败，请重新再试'
            }))
        return HttpResponse(json.dumps({
            'result': '申请已提交'
        }))
    else:
        return HttpResponse(json.dumps({
            'result': '提交失败，请重新再试'
        }))


# 签到模块发送邮件功能
def publish_sign(request):
    signPassword = request.POST.get('signPassword')
    l_id = request.POST.get('l_id')
    p_id = request.user
    try:
        P = sign_publish.objects.get(l_id=l_id, p_id=p_id)
        P.signPassword = signPassword
        P.save()
    except sign_publish.DoesNotExist:
        sign_publish.objects.update_or_create(
            signPassword=signPassword,
            l_id=l_id,
            p_id=p_id
        )
    for i in Reserved_Lecture.objects.filter(lecture_id=l_id).values():
        user = Register_UserInfo.objects.get(Username=i['user_id'])
        serializer = Serializer(settings.SECRET_KEY, 600)
        userinfo = {'confirm': user.Username}
        token1 = serializer.dumps(userinfo)
        token = token1.decode()
        # 使用celery异步发送邮件
        send_lisener_inlecture_email.delay(user.Email, l_id, token)
        print(1)
    return HttpResponse(json.dumps({
        'result': '发布成功'
    }))
