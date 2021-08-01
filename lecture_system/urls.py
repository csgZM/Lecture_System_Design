from django.conf.urls import url
from lecture_system import views

urlpatterns = [
    # 路径为空的要放到下面，路径带有数据的也要放到下面
    url(r'^sign/(?P<l_id>\w+)/(?P<token>.*)$', views.signView.as_view()),
    url(r'^reserve', views.reserve, name='reserve'),
    url(r'^publish', views.PublishView.as_view(), name='publish'),
    url(r'^lecture_detail/(?P<list_category>\w+)/(?P<list_id>\w+)',
        views.Lecture_detailView.as_view(), name='Ldetail'),
    url(r'^lecture_detail/Pname=(?P<Pname>\w+)', views.List_nameView.as_view(), name='list_name'),
    url(r'^lecture_detail/(?P<list_category>\w+)', views.ListView.as_view(), name='list'),
    url(r'^', views.LectureView.as_view(), name='index'),
]
