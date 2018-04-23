'''为应用程序users定义URL模式'''
from  django.conf.urls import url
from . import views

urlpatterns = [
    # 登陆页面
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register, name='register'),
]
app_name = 'users'
