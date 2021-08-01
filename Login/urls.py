from django.conf.urls import url
from Login import views

urlpatterns = [
    url(r'^check_bindemail', views.check_bindemail, name='check_bindemail'),
    url(r'fpassword', views.Forgetpassword.as_view(), name='fpassword'),
    url('^regist', views.RegistView.as_view(), name='regist'),
    url(r'^success/', views.regist_success, name='submit'),
    url(r'^rt_l/', views.ReturnLoginView.as_view(), name="rt_l"),
    url(r'^checkusername', views.checkusername, name='checkusername'),
    url(r'^checkpassword', views.checkpassword, name='checkpassword'),
    url(r'^checkphone', views.checkphonenumber, name='checkphone'),
    url(r'^checkemail', views.checkemail, name='checkemail'),
    url(r'^$', views.FirstView.as_view(), name='login'),
]
