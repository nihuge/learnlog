from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import translation


# Create your views here.
def logout_view(request):
    '''注销用户'''
    logout(request)
    return HttpResponseRedirect(reverse('learnlogs:index'))


def login_view(request):
    '''用户登陆'''
    if request.method != 'POST':
        # 显示空的登陆表单
        translation.activate(
            request.session.get('django_language', translation.get_language()))
        form = AuthenticationForm()
    else:
        # 处理填写好的表单
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            # 让用户自动登录，再重定向到主页
            authenticate_user = authenticate(
                username=request.POST['username'], password=request.POST['password'])
            login(request, authenticate_user)
            return HttpResponseRedirect(reverse('learnlogs:index'))

    context = {'form': form}
    return render(request, 'user/login.html', context)


def register(request):
    '''注册新用户'''
    if request.method != 'POST':
        # 显示空的注册表单
        translation.activate(
            request.session.get('django_language', translation.get_language()))
        form = UserCreationForm()
    else:
        # 处理填写好的表单
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # 让用户自动登录，再重定向到主页
            authenticate_user = authenticate(
                username=new_user.username, password=request.POST[
                    'password1'])
            login(request, authenticate_user)
            return HttpResponseRedirect(reverse('learnlogs:index'))

    context = {'form': form}
    return render(request, 'user/register.html', context)
