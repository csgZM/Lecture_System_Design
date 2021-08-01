from django.conf.urls import url
from User import views

urlpatterns = [
    url(r'^getpublish', views.getpublish, name='getpublish'),
    url(r'^lecture_experience', views.Lecture_ExperienceView.as_view(), name='lecture_experience'),
    url(r'^l_experience', views.experience, name='l_experience'),
    url(r'^publish_sign', views.publish_sign, name='publish_sign'),
    url(r'^rname', views.rname, name='rname'),
    url(r'^loginout', views.logout_view, name='loginout'),
    url(r'^checkrpassword', views.checkrpassowrd, name='checkrpassword'),
    url(r'^rpassword', views.RpasswordView.as_view(), name='rpassword'),
    url(r'', views.IndexView.as_view(), name='index'),
]
