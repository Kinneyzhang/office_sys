# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
# from django.core import serializers
from .models import User, QuizBank, Post, PostTag
import json

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from django.db.models import Count

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload/quiz_bank/')


@csrf_exempt
def register(request):
    user_info = json.loads(request.body.decode())
    msg = ""
    # Printe(user_info)
    new_username = user_info["new_username"]
    new_password1 = user_info["new_password1"]
    new_password2 = user_info["new_password2"]

    try:
        User.objects.get(userName=new_username)
    except User.DoesNotExist:
        if new_password1 == new_password2:
            msg = "账号注册成功!"
            u = User(userName=new_username, userPasswd=new_password1)
            u.save()
        else:
            msg = "两次密码输入不匹配！"
    else:
        msg = "该用户已存在！"

    # message = serializers.serialize('json', Queryset)
    # safe=False, 序列化非字典对象时使用

    return JsonResponse({"msg": msg})


def login(request):
    user_info = json.loads(request.body.decode())
    msg = ""
    username = user_info["username"]
    password = user_info["password"]
    userid = 0
    islogin = False

    request.session.flush()
    # if request.session.get('is_login', True):
    #     return JsonResponse({"msg": "you have already login!"})
    # if request.method == 'POST':

    try:
        u = User.objects.get(userName=username)
    except User.DoesNotExist:
        msg = "该用户未注册！"
    else:
        if password == u.userPasswd:
            islogin = True
            userid = User.objects.get(userName=username).id
            msg = "登陆成功！"
        else:
            msg = "密码输入错误！"

    return JsonResponse(
        {
            "msg": msg, "user_id": userid,
            "user_name": username, "is_login": islogin
        }
    )


def show_quiz(request):
    quiz = QuizBank.objects.all()
    quiz_list = list(quiz.values('quizId', 'quizText'))

    return JsonResponse(json.dumps(quiz_list), safe=False)


def download(request):
    req = json.loads(request.body.decode())
    quizId = req["quiz_id"]
    filename = QuizBank.objects.get(quizId=quizId).quizFilename
    file = open(os.path.join(MEDIA_ROOT, '%s') % filename, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s.zip"' % filename
    return response


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return os.path.join("userup", instance.stu.id, filename)


def upload(request):
    if request.method == 'POST':
        fileObj = request.FILES.get('file')
        # print(json.dumps(fileObj))
        # userid = request.FILES.get('userid')
        f = open(os.path.join(BASE_DIR, 'upload', 'userup', fileObj.name),'wb')
        for chunk in fileObj.chunks():
            f.write(chunk)
        f.close()
        return JsonResponse({'msg': 'OK'})


def create_post(request):
    req = json.loads(request.body.decode())
    postUser = req["postUser"]
    postTitle = req["postTitle"]
    postTag = req["postTag"]
    postContent = req["postContent"]
    postTag = PostTag.objects.get(postTag=postTag)
    postUser = User.objects.get(userName=postUser)
    post = Post(
        postTag=postTag, postTitle=postTitle,
        postContent=postContent, postPerson=postUser
    )
    post.save()
    return JsonResponse({"msg": "post create successfully!"})


def get_post(request):
    post = Post.objects.all()
    # 获取帖子回复的数量
    
    # 计算帖子了多长时间
    post_list = list(post.values(
        'postPerson', 'postTitle',
        'postTag', 'postContent',
    ))
    return JsonResponse(json.dumps(post_list), safe=False)


def get_tagNum(request):
    # 获取每类标签的帖子的数量
    TagNumList = []
    num = 0
    TagSet = PostTag.objects.all()
    for t in TagSet:  # 直接遍历QuerySet
        if t is None:
            num = 0  # 没有帖子的标签查询不到
        else:
            # Post模型中的postTag是外键,不是数据字符串
            num = len(Post.objects.filter(postTag=t))
            print(num)
        TagNumList.append({"tagName": str(t), "tagNum": num})

    return JsonResponse(json.dumps(TagNumList), safe=False)
