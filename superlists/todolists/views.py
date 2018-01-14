from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    # 不要在python代码中用字符串创建html，使用模板函数调用html模板文件
    # 要先在superlists/settings.INSTALLED_APPS里添加此todolists
    return render(request, 'home.html',{'new_item_text': request.POST.get('item_text', '')})


def index(request):
    return HttpResponse("<h1>Welcome to the to-do lists app</h1>")
