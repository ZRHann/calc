import re
from django.shortcuts import render, redirect, HttpResponse
import requests
import random
import json
from app01.tools import mathrepl
from django.views.decorators.csrf import csrf_exempt
from app01.models import UserInfo
from app01.models import ArticleInfo
import time
import string
from app01.tools import GetBeijingTime
# 传入request，判断是否有已登录的Cookie


def getUsername(request):
    CKusername = request.COOKIES.get('username')
    CKpassword = request.COOKIES.get('password')
    obj = UserInfo.objects.filter(username=CKusername).first()
    # print(obj)
    if not obj:
        return -1
    if obj.password != CKpassword:
        return -1
    return CKusername


def index(request):
    currentUsername = getUsername(request)
    ArticleList = ArticleInfo.objects.all().order_by('-PostTime')
    Dict = {
        'ArticleList': ArticleList,
        'currentUsername': currentUsername,
    }
    return render(request, 'index.html', Dict)


def BingPic(request):
    currentUsername = getUsername(request)
    # print(currentUsername)
    idx = random.randint(-1, 10)
    bing_api = "https://global.bing.com"
    header = {
        "Origin": bing_api,
        "Host": bing_api.replace("https://", ""),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.110 Safari/537.36 Edge/14.16299",
        "Referer": bing_api
    }
    url = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=' + str(idx) + '&n=1'
    # print(url)
    code = requests.get(url=url, headers=header).text
    dictcode = json.loads(code)
    imgCopyrighten = re.findall(r' \(©.+', dictcode['images'][0]['copyright'])[0]
    Dict = {
        'imgUrl': 'https://cn.bing.com' + dictcode['images'][0]['url'],
        'imgCopyright': dictcode['images'][0]['copyright'].replace(imgCopyrighten, ''),
        'imgCopyrighten': imgCopyrighten,
        'imgCopyrightlink': dictcode['images'][0]['copyrightlink'],
        'imgTitle': dictcode['images'][0]['title'],
        'currentUsername': currentUsername,
    }
    return render(request, 'BingPic.html', Dict)


def empty(request):
    return redirect('index/')


def yyec_equations(request):
    currentUsername = getUsername(request)
    return render(request, 'yyec_equations.html', {'currentUsername': currentUsername})


def games_jingChess(request):
    currentUsername = getUsername(request)
    return render(request, 'jingChess.html', {'currentUsername': currentUsername})


def function(request):
    currentUsername = getUsername(request)
    return render(request, 'function.html', {'currentUsername': currentUsername})


@csrf_exempt
def function_ajax(request):
    fxbox = request.POST.get('fxbox')
    xbox = request.POST.get('xbox')
    if mathrepl.is_number(xbox):
        answer = mathrepl.calculateFx(fxbox, float(xbox))
        Dict = {
            'fxbox': fxbox,
            'xbox': xbox,
            'answer': answer
        }
        return HttpResponse(json.dumps(Dict))
    else:
        Dict = {
            'fxbox': fxbox,
            'xbox': xbox,
            'answer': 'ERR-3       自变量x非实数'
        }
        return HttpResponse(json.dumps(Dict))


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
    print(request.POST)
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


@csrf_exempt
def logout_ajax(request):
    response = HttpResponse("success")
    response.delete_cookie('username')
    response.delete_cookie('password')
    return response


def changePassword(request):
    currentUsername = getUsername(request)
    return render(request, 'changePassword.html', {'currentUsername': currentUsername})


@csrf_exempt
def changePassword_ajax(request):
    CKusername = getUsername(request)
    OldPassword = request.POST['OldPassword']
    NewPassword = request.POST['NewPassword']
    if not CKusername:
        return HttpResponse('Please Login First')
    else:
        obj = UserInfo.objects.filter(username=CKusername).first()
        realPassword = obj.password
        if OldPassword != realPassword:
            return HttpResponse('Wrong OldPassword')
        UserInfo.objects.filter(username=CKusername).update(password=NewPassword)
        response = HttpResponse('Success')
        response.delete_cookie('username')
        response.delete_cookie('password')
        return response


def AddArticle(request):
    currentUsername = getUsername(request)
    Dict = {
        'currentUsername': currentUsername,
    }
    return render(request, 'AddArticle.html', Dict)


@csrf_exempt
def AddArticle_ajax(request):
    currentUsername = getUsername(request)
    if currentUsername == -1:
        return HttpResponse('Please Login')
    title = request.POST['title']
    content = request.POST['content']
    PostTime = time.strftime('%Y-%m-%d %H:%M:%S', GetBeijingTime.getBeijingTime())
    seed = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    # print(seed)
    username = currentUsername
    ArticleInfo.objects.create(title=title, content=content, seed=seed, username=username, PostTime=PostTime)
    return HttpResponse('Article successfully added')


def MyArticle(request):
    currentUsername = getUsername(request)
    ArticleList = ArticleInfo.objects.filter(username=currentUsername).order_by('-PostTime')
    Dict = {
        'currentUsername': currentUsername,
        'ArticleList': ArticleList,
    }
    return render(request, 'MyArticle.html', Dict)


@csrf_exempt
def DeleteArticle_ajax(request):
    currentUsername = getUsername(request)
    if currentUsername == -1:
        return HttpResponse('Please Login')
    PostTime = request.POST['PostTime']
    seed = request.POST['seed']
    ArticleInfo.objects.filter(PostTime=PostTime, seed=seed).delete()
    return HttpResponse('Successfully Deleted')


def ViewArticle(request):
    currentUsername = getUsername(request)
    PostTime = request.GET['PostTime']
    seed = request.GET['seed']
    article = ArticleInfo.objects.filter(PostTime=PostTime, seed=seed).first()
    Dict = {
        'currentUsername': currentUsername,
        'article': article,
    }
    return render(request, 'ViewArticle.html', Dict)


def games_test1(request):
    currentUsername = getUsername(request)
    Dict = {
        'currentUsername': currentUsername,
    }
    return render(request, 'test1/index.html', Dict)


def games(request):
    currentUsername = getUsername(request)
    Dict = {
        'currentUsername': currentUsername,
    }
    return render(request, 'games.html', Dict)


def games_csgov01(request):
    currentUsername = getUsername(request)
    Dict = {
        'currentUsername': currentUsername,
    }
    return render(request, 'csgov01/index.html', Dict)


def games_csgov02(request):
    currentUsername = getUsername(request)
    Dict = {
        'currentUsername': currentUsername,
    }
    return render(request, 'csgov02/index.html', Dict)


def games_csgov03(request):
    currentUsername = getUsername(request)
    Dict = {
        'currentUsername': currentUsername,
    }
    return render(request, 'csgov03/index.html', Dict)


def games_csgov04(request):
    currentUsername = getUsername(request)
    Dict = {
        'currentUsername': currentUsername,
    }
    return render(request, 'csgov04/index.html', Dict)


def ChattingRoom(request):
    currentUsername = getUsername(request)
    Dict = {
        'currentUsername': currentUsername,
    }
    return render(request, 'ChattingRoom.html', Dict)


def planet(request):
    currentUsername = getUsername(request)
    Dict = {
        'currentUsername': currentUsername,
    }
    return render(request, 'planet.html', Dict)