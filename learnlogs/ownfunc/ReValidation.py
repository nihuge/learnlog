import re
from django.conf import settings


def check_domian_legitimacy(url):
    # 正则验证domian
    a = re.search(
        r'^https?://([a-zA-Z0-9\.\-]+)\:?(?:\d+)?/\S+$',
        url)
    # 得到正则匹配到的domian
    if a:
        urldomian = a.group(1)
    else:
        urldomian = ''
    # 判断是否是注册的域名
    print(urldomian)
    if urldomian in settings.ALLOWED_HOSTS:
        return True

    return False
