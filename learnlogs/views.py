from django.shortcuts import render
from .models import Topic, Entry, I18n
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .form import TopicForm, EntryForm
from django.conf import settings
# from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from learnlogs.ownfunc.ReValidation import check_domian_legitimacy


# Create your views here.
def index(request):
    '''学习笔记的主页'''
    return render(request, 'learnlogs/index.html')


@login_required
def topics(request):
    '''显示所有的主题'''
    topics = Topic.objects.filter(owner=request.user).order_by('-date_add')
    context = {'topics': topics}
    return render(request, 'learnlogs/topics.html', context)


@login_required
def topic(request, topic_id):
    '''显示单个主题及所有的条目'''
    topic = Topic.objects.get(id=topic_id)
    # 确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learnlogs/topic.html', context)


@login_required
def new_topic(request):
    '''添加新主题'''
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        translation.activate(request.session.get('django_language',translation.get_language()))
        form = TopicForm()
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learnlogs:topics'))

    context = {'form': form}
    return render(request, 'learnlogs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    '''在特定的主题中添加新条目'''
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 未提交数据，创建一个空表单
        translation.activate(request.session.get('django_language', translation.get_language()))
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learnlogs:topic',
                                                args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learnlogs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    '''
    编辑既有条目
    :param request:
    :param entry_id:
    :return:
    '''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # 初次请求建立表单
        translation.activate(request.session.get('django_language',translation.get_language()))
        form = EntryForm(instance=entry)
    else:
        # POST提交数据就对其进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learnlogs:topic',
                                                args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learnlogs/edit_entry.html', context)


def change_language(request, language):
    '''更改语言'''
    languages = settings.LANGUAGE_LIST
    #判断语言是否是注册过的
    if language in languages.keys():
        request.session['language'] = language
        request.session['django_language'] = language
    #判断从哪里跳转过来的
    if 'HTTP_REFERER' in request.META:
        url = request.META['HTTP_REFERER']
        #验证域名的合法性，是否是注册的域名，如果不是则跳转回首页
        if not check_domian_legitimacy(url):
            url = reverse('learnlogs:index')
    else:
        #如果找不到就跳转回首页
        url = reverse('learnlogs:index')
    return HttpResponseRedirect(url)
