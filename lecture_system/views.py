from django.shortcuts import render, HttpResponse, reverse, redirect
from django.views.generic import View
from lecture_system.models import Lecture_Message
from Login.models import Reserved_Lecture, Register_UserInfo, UserToken, Published_Lecture, Listened_Lecture
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage  # 分页相关的包
from User.models import sign_publish
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  # 信息加密
from django.conf import settings
from itsdangerous import SignatureExpired  # 设置密钥的时间后，超过该时间所报的错误
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator  # 装饰器
from django.contrib.auth.decorators import login_required
from django.core.cache import cache


# Create your views here.
class LectureView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        data = {"status": 200, "data": {}}
        name = Register_UserInfo.objects.filter(Username=request.user).values()[0]["nikename"]
        c = cache.get(name)
        if c:
            list_kj = c["list_kj"]
            list_fl = c["list_fl"]
            list_wx = c["list_wx"]
            list_lz = c["list_lz"]
            list_sz = c["list_sz"]
            list_sx = c["list_sx"]
            print("cccccccccccccc")
        else:
            list_kj = Lecture_Message.objects.filter(Lecture_category='kj').values()[::-1][1:4]
            list_fl = Lecture_Message.objects.filter(Lecture_category='fl').values()[::-1][1:4]
            list_wx = Lecture_Message.objects.filter(Lecture_category='wx').values()[::-1][1:4]
            list_lz = Lecture_Message.objects.filter(Lecture_category='lz').values()[::-1][1:4]
            list_sz = Lecture_Message.objects.filter(Lecture_category='sz').values()[::-1][1:4]
            list_sx = Lecture_Message.objects.filter(Lecture_category='jk').values()[::-1][1:4]
            data["data"] = {
                'list_kj': list_kj, 'list_fl': list_fl, 'list_wx': list_wx, 'list_lz': list_lz,
                'list_sz': list_sz, 'list_sx': list_sx,
            }
            cache.set(name, data["data"], timeout=None)
            print("aaaaaaaaaaaaaa")
        return render(request, 'lecture_page.html',
                      {'list_kj': list_kj, 'list_fl': list_fl, 'list_wx': list_wx, 'list_lz': list_lz,
                       'list_sz': list_sz, 'list_jk': list_sx,
                       'name': name,
                       })


class Lecture_detailView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if Reserved_Lecture.objects.filter(lecture_id=kwargs['list_id']).count():
            RN = Reserved_Lecture.objects.filter(lecture_id=kwargs['list_id']).count()
        else:
            RN = 0
        name = Register_UserInfo.objects.filter(Username=request.user).values()[0]["nikename"]
        p = Lecture_Message.objects.filter(id=kwargs['list_id'], Lecture_category=kwargs['list_category']).values()
        Lecture_data = p[0]['Lecture_Stime'].split(" ")[1]
        Lecture_Stime = p[0]['Lecture_Stime'].split(" ")[0]
        Lecture_Etime = p[0]['Lecture_Etime'].split(" ")[0]
        max_reserve = p[0]["Lecture_SN"]
        if p[0]['Lecture_category'] == 'kj':
            category = '科技'
        elif p[0]['Lecture_category'] == 'wx':
            category = '文学'
        elif p[0]['Lecture_category'] == 'fl':
            category = '法律'
        elif p[0]['Lecture_category'] == 'lz':
            category = '励志'
        elif p[0]['Lecture_category'] == 'sz':
            category = '素质教育'
        elif p[0]['Lecture_category'] == 'jk':
            category = '身心健康'
        return render(request, 'lecture_details.html', {'detail': p[0],
                                                        'name': name,
                                                        'Lecture_data': Lecture_data,
                                                        'Lecture_Stime': Lecture_Stime,
                                                        'Lecture_Etime': Lecture_Etime,
                                                        'user_id': json.dumps(str(request.user)),
                                                        'l_id': json.dumps(kwargs['list_id']),
                                                        'RN': RN,
                                                        'max_reserve': json.dumps(max_reserve),
                                                        'category': category
                                                        })


class ListView(View):  # 按讲座类别排列的列表页
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if kwargs['list_category'] == 'kj':
            category = '科技'
        if kwargs['list_category'] == 'wx':
            category = '文学'
        if kwargs['list_category'] == 'fl':
            category = '法律'
        if kwargs['list_category'] == 'lz':
            category = '励志'
        if kwargs['list_category'] == 'sz':
            category = '素质教育'
        if kwargs['list_category'] == 'jk':
            category = '身心健康'
        list = Lecture_Message.objects.filter(Lecture_category=kwargs['list_category']).order_by('-id')
        paginator = Paginator(list, 2)
        page = request.GET.get('page')
        try:
            if int(page) > int(paginator.num_pages):
                contacts = paginator.page(1)
            else:
                contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(1)
        except InvalidPage:  # 超过最大页数跳到第一页
            contacts = paginator.page(1)
            # todo: 进行页码的控制，页面上最多显示5个页码
            # 1.总页数小于5页，页面上显示所有页码
            # 2.如果当前页是前3页，显示1-5页
            # 3.如果当前页是后3页，显示后5页
            # 4.其他情况，显示当前页的前2页，当前页，当前页的后2页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        return render(request, 'list.html', {
            'contacts': contacts,
            'category': category,
            'list_page': pages,
            'category_value': kwargs['list_category'],
            'Username': request.user,
        })


class List_nameView(View):  # 按主讲人排列的列表页
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        list = Lecture_Message.objects.filter(Lecture_Pname=kwargs['Pname']).values()
        return render(request, 'list_name.html', {
            'list': list,
        })


class PublishView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        U = UserToken.objects.filter(user_id=str(request.user)).first()
        print("publishpower:", U.publish_power)
        if U.publish_power == '' or U.publish_power == '0':
            publish_power = ''
        else:
            publish_power = U.publish_power
        return render(request, 'publish.html', {
            'publish_power': publish_power
        })

    def post(self, request):  # 异步讲座发布视图函数
        Stime = " ".join([request.POST.get('Stime'), request.POST.get('data')])
        Etime = " ".join([request.POST.get('Etime'), request.POST.get('data')])

        lecture = Lecture_Message(Lecture_title=request.POST.get('title'), Lecture_Pname=request.POST.get('Pname'),
                                  Lecture_introdution=request.POST.get('introdution'),
                                  Lecture_SN=request.POST.get('SN'),
                                  Lecture_category=request.POST.get('category'), Lecture_Stime=Stime,
                                  Lecture_Etime=Etime, Lecture_Location=request.POST.get('Location'))
        lecture.save()
        lecture_id = Lecture_Message.objects.filter(Lecture_title=request.POST.get('title'),
                                                    Lecture_Pname=request.POST.get('Pname')).values()[0]['id']
        Published_Lecture.objects.update_or_create(
            user_id=UserToken.objects.filter(token=str(request.user)).first(),
            lecture_id=lecture_id
        )
        return HttpResponse(json.dumps({
            'result': '发布成功'
        }))


def reserve(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        l_id = request.POST.get('l_id')
        max_reserve = request.POST.get('max_reserve')
        print(f"用户id：{user_id} 讲座id:{l_id}")
    if Reserved_Lecture.objects.filter(lecture_id=l_id, user_id=user_id).count():
        return HttpResponse(json.dumps(
            {
                'message': '你已预定，请勿重复预定',
            }))

    elif Reserved_Lecture.objects.filter(lecture_id=l_id).count() >= int(max_reserve):
        return HttpResponse(json.dumps(
            {
                'message': '预定人数已满',
            }))

    else:
        Reserved_Lecture.objects.update_or_create(
            user_id=user_id,
            lecture_id=l_id
        )
        R = Reserved_Lecture.objects.filter(lecture_id=l_id).count()
        return HttpResponse(json.dumps(
            {
                'message': '预定成功',
                'R': R
            }))


class signView(View):
    def get(self, request, l_id, token):  # 签到界面
        return render(request, 'sign.html')

    def post(self, request, l_id, token):
        serializer = Serializer(settings.SECRET_KEY, 600)  # 将用户名消息进行加密
        try:
            userinfo = serializer.loads(token)  # 获取要签到的用户名
            username = userinfo['confirm']
            try:
                if Listened_Lecture.objects.filter(user_id=username, lecture_id=l_id):
                    return HttpResponse("您已签到,请勿重复签到")
                else:
                    if request.POST.get('signPassword') == sign_publish.objects.filter(l_id=l_id).values()[0][
                        'signPassword']:
                        print(sign_publish.objects.filter(l_id=l_id).values()[0]['signPassword'])
                        Listened_Lecture.objects.update_or_create(user_id=username, lecture_id=l_id)
                        return HttpResponse('签到成功')
                    else:
                        return HttpResponse('签到码错误')
            except Exception as e:
                return HttpResponse(e)
        except SignatureExpired as e:
            return HttpResponse("签到已过期")  # 签到已过期
