import re
from django.shortcuts import render, redirect, HttpResponse
import requests
import random
import json
from app01 import mathrepl
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from app01.models import UserInfo


# 传入request，判断是否有已登录的Cookie
def getUsername(request):
    CKusername = request.COOKIES.get('username')
    CKpassword = request.COOKIES.get('password')
    obj = UserInfo.objects.filter(username=CKusername).first()
    if not obj:
        return -1
    if obj.password != CKpassword:
        return -1
    return CKusername


def index(request):
    currentUsername = getUsername(request)
    print(currentUsername)
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
        'imgTitle': dictcode['images'][0]['title'],
        'currentUsername': currentUsername,
    }
    return render(request, 'index.html', dict)


def empty(request):
    currentUsername = getUsername(request)
    return redirect('index/')


def yyec_equations(request):
    currentUsername = getUsername(request)
    return render(request, 'yyec_equations.html', {'currentUsername': currentUsername})


def jingChess(request):
    currentUsername = getUsername(request)
    return render(request, 'jingChess.html', {'currentUsername': currentUsername})


def function(request):
    currentUsername = getUsername(request)
    return render(request, 'function.html', {'currentUsername': currentUsername})



@csrf_exempt
def function_ajax(request):
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
    currentUsername = getUsername(request)
    return render(request, 'matrix.html', {'currentUsername': currentUsername})


def login(request):
    currentUsername = getUsername(request)
    return render(request, 'login.html', {'currentUsername': currentUsername})


def register(request):
    currentUsername = getUsername(request)
    return render(request, 'register.html', {'currentUsername': currentUsername})


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
        UserInfo.objects.create(username=username, password=password)
        return HttpResponse('success')


@csrf_exempt
def login_ajax(request):
    username = request.POST['username']
    password = request.POST['password']
    row_obj = UserInfo.objects.filter(username=username).first()
    if not row_obj:
        return HttpResponse('username not exist')
    if row_obj.password != password:
        return HttpResponse('wrong password')
    response = HttpResponse('success')
    response.set_cookie('username', username, expires=60*60*24*30*12*100)
    response.set_cookie('password', password, expires=60*60*24*30*12*100)
    return response


