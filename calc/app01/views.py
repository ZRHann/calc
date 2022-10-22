import re
from django.shortcuts import render, redirect, HttpResponse
import requests
import random
import json
from app01 import mathrepl
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from app01.models import UserInfo


def index(request):
    idx = random.randint(-1, 10)
    bing_api = "https://global.bing.com"
    header = {
        "Origin": bing_api,
        "Host": bing_api.replace("https://", ""),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/14.16299",
        "Referer": bing_api
    }
    url = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=' + str(idx) + '&n=1'
    # print(url)
    code = requests.get(url=url, headers=header).text
    dictcode = json.loads(code)
    imgCopyrighten = re.findall(r' \(©.+', dictcode['images'][0]['copyright'])[0]
    dict = {
        'imgUrl': 'https://cn.bing.com' + dictcode['images'][0]['url'],
        'imgCopyright': dictcode['images'][0]['copyright'].replace(imgCopyrighten, ''),
        'imgCopyrighten': imgCopyrighten,
        'imgCopyrightlink': dictcode['images'][0]['copyrightlink'],
        'imgTitle': dictcode['images'][0]['title']
    }
    return render(request, 'index.html', dict)


def empty(request):
    return redirect('index/')


def yyec_equations(request):
    return render(request, 'yyec_equations.html')


def jingChess(request):
    return render(request, 'jingChess.html')


def function(request):
    return render(request, 'function.html')



@csrf_exempt
def function_ajax(request):
    # return HttpResponse(1)
    fxbox = request.POST.get('fxbox')
    xbox = request.POST.get('xbox')
    dict = {}
    if mathrepl.is_number(xbox):
        answer = mathrepl.calculateFx(fxbox, float(xbox))
        dict = {
            'fxbox': fxbox,
            'xbox': xbox,
            'answer': answer
        }
    else:
        dict = {
            'fxbox': fxbox,
            'xbox': xbox,
            'answer': 'ERR-3       自变量x非实数'
        }
    return HttpResponse(json.dumps(dict))


def matrix(request):
    return render(request, 'matrix.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


@csrf_exempt
def register_ajax(request):
    # print(request.POST)
    username = request.POST['username']

    print(username)
    password = request.POST['password']
    row_obj = UserInfo.objects.filter(username=username).first()
    if row_obj:
        return HttpResponse('username exist')
    else:
        return HttpResponse('success')


