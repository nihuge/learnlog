from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class Topic(models.Model):
    '''用户学习的主题'''
    text = models.CharField(max_length=200)
    date_add = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        '''返回模型的字符串'''
        return self.text


class Entry(models.Model):
    '''学到的有关某个主题的具体知识'''
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        '''返回模型的字符串'''
        return self.text[:50] + "..."


class I18n(models.Model):
    '''国际化语言'''
    Language_Chiose = settings.LANGUAGES
    language = models.CharField(max_length=8, choices=Language_Chiose,
                                default='zh-hans')
    untranslated_text = models.TextField()
    translated_text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        '''设置联合唯一属性'''
        unique_together = ('language', 'untranslated_text')

    def __str__(self):
        '''返回模型的字符串'''
        return self.language
