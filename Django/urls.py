"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from lecture_system import views
from django.conf.urls import url, include

urlpatterns = [
    url(r'^search/', include('haystack.urls')),  # 全文检索框架
    url(r'^admin/', admin.site.urls),
    url(r'^user_detail/', include(('User.urls', 'User'), namespace='User')),
    url(r'^lecture_index/', include(('lecture_system.urls', 'lecture_system'), namespace='lecture_system')),
    url(r'^', include(('Login.urls', 'Login'), namespace='Login')),
]
