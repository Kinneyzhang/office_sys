# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
# from django.core import serializers
from .models import User, QuizType, QuizBank, Post, PostTag, PostReply, ExerRecord, KnowledgePoint
import json
import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload/quiz_bank/')


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


# 注册登陆 ##############################################################

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

    return JsonResponse({"msg": msg})


def login(request):
    user_info = json.loads(request.body.decode())
    msg = ""
    username = user_info["username"]
    password = user_info["password"]
    userid = 0
    islogin = False
    registertime = ""

    request.session.flush()

    try:
        u = User.objects.get(userName=username)
    except User.DoesNotExist:
        msg = "该用户未注册！"
    else:
        if password == u.userPasswd:
            islogin = True
            userid = User.objects.get(userName=username).id
            registertime = User.objects.get(userName=username).registerTime.strftime('%Y-%m-%d %H:%I:%S')
            print(registertime)
            msg = "登陆成功！"
        else:
            msg = "密码输入错误！"

    return JsonResponse(
        {
            "msg": msg, "user_id": userid,
            "user_name": username, "is_login": islogin,
            "register_time": registertime,
        }
    )


# 试题展示 ##############################################################

def get_quiz(request):
    quiz = QuizBank.objects.all()
    quiz_list = []
    uploadNum = 0
    for q in quiz:
        accuracy = 1.0
        temp = 0
        # 获取试题的知识点
        # 计算平均正确率
        knowledgePoint = list(q.quizKnowledgePoint.all().values('knowledgePoint'))
        try:
            record = ExerRecord.objects.filter(quiz=q).filter(correctStatus=True)
            uploadNum = len(ExerRecord.objects.filter(quiz=q).filter(uploadStatus=True))

            for r in record:
                temp += (r.quizScore / q.quizFullScore)
                print("平均数之和：%s" % temp)
            try:
                accuracy = round(temp / len(record), 4)
                print("正确率：%s" % accuracy)
                print("记录条数：%s" % len(record))
            except ZeroDivisionError:
                pass
        except ExerRecord.DoesNotExist:
            accuracy = 1.0
            pass

        quiz_list.append({
            'quizId': q.quizId,
            'quizText': q.quizText,
            'knowledgePoint': knowledgePoint,
            'uploadNum': uploadNum,
            'accuracy': accuracy,
        })
    return JsonResponse(json.dumps(quiz_list), safe=False)


def get_type_list(request):
    type_list = []
    typeSet = QuizType.objects.all()
    for t in typeSet:
        type_list.append(t.quizTypeName)
    return JsonResponse(json.dumps(type_list), safe=False)


# 获取综合知识点的试题
def get_type_quiz(request):
    req = json.loads(request.body.decode())
    quiz_type = req["quiz_type"]
    print(quiz_type)
    quiz = None
    try:
        quiz = QuizBank.objects.filter(quizType=QuizType.objects.get(quizTypeName=quiz_type)).filter(quizPointNum='many')
    except quiz.DoesNotExist:
        return JsonResponse({"msg": "没有%s试题" % quiz_type})
    else:
        quiz_list = []
        uploadNum = 0
        for q in quiz:
            accuracy = 1.0
            temp = 0
            # 获取试题的知识点
            # 计算平均正确率
            knowledgePoint = list(q.quizKnowledgePoint.all().values('knowledgePoint'))
            try:
                record = ExerRecord.objects.filter(quiz=q).filter(correctStatus=True)
                uploadNum = len(ExerRecord.objects.filter(quiz=q).filter(uploadStatus=True))
                
                for r in record:
                    temp += (r.quizScore / q.quizFullScore)
                    print("平均数之和：%s" % temp)
                    try:
                        accuracy = round(temp / len(record), 4)
                        print("正确率：%s" % accuracy)
                        print("记录条数：%s" % len(record))
                    except ZeroDivisionError:
                        pass
            except ExerRecord.DoesNotExist:
                accuracy = 1.0
                pass
            
            quiz_list.append({
                'quizId': q.quizId,
                'quizText': q.quizText,
                'knowledgePoint': knowledgePoint,
                'uploadNum': uploadNum,
                'accuracy': accuracy,
            })

        return JsonResponse(json.dumps(quiz_list), safe=False)


# 获取单一知识点的试题
def get_point_quiz(request):
    req = json.loads(request.body.decode())
    quiz_type = req["quiz_type"]
    knowledge_point = req["knowledge_point"]
    quiz = None
    try:
        quiz = QuizBank.objects.filter(quizType=QuizType.objects.get(quizTypeName=quiz_type)).filter(quizPointNum='one').filter(quizKnowledgePoint__knowledgePoint=knowledge_point)
    except QuizBank.DoesNotExist:
        return JsonResponse({"msg": "没有%s试题" % quiz_type})
    else:
        quiz_list = []
        uploadNum = 0
        for q in quiz:
            accuracy = 1.0
            temp = 0
            # 获取试题的知识点
            # 计算平均正确率
            knowledgePoint = list(q.quizKnowledgePoint.all().values('knowledgePoint'))
            try:
                record = ExerRecord.objects.filter(quiz=q).filter(correctStatus=True)
                uploadNum = len(ExerRecord.objects.filter(quiz=q).filter(uploadStatus=True))
                
                for r in record:
                    temp += (r.quizScore / q.quizFullScore)
                    print("平均数之和：%s" % temp)
                    try:
                        accuracy = round(temp / len(record), 4)
                        print("正确率：%s" % accuracy)
                        print("记录条数：%s" % len(record))
                    except ZeroDivisionError:
                        pass
            except ExerRecord.DoesNotExist:
                accuracy = 1.0
                pass
            
            quiz_list.append({
                'quizId': q.quizId,
                'quizText': q.quizText,
                'knowledgePoint': knowledgePoint,
                'uploadNum': uploadNum,
                'accuracy': accuracy,
            })

        return JsonResponse(json.dumps(quiz_list), safe=False)


def get_knowledge_point(request):
    knowledge_list = []
    req = json.loads(request.body.decode())
    quizType = req["quiz_type"]
    knowledgeSet =  KnowledgePoint.objects.filter(quizType=QuizType.objects.get(quizTypeName=quizType))
    for k in knowledgeSet:
        knowledge_list.append(k.knowledgePoint)
        
    return JsonResponse(json.dumps(knowledge_list), safe=False)


# 上传下载 ##################################################################

def download(request):
    req = json.loads(request.body.decode())
    quizId = req["quiz_id"]
    userId = req["user_id"]

    filename = QuizBank.objects.get(quizId=quizId).quizFilename
    file = open(os.path.join(MEDIA_ROOT, '%s') % filename, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s.zip"' % filename

    ExerRecord.objects.create(
        user=User.objects.get(pk=userId),
        quiz=QuizBank.objects.get(quizId=quizId),
    )

    return response


def upload(request):
    fileObj = request.FILES.get('file')
    user_id = request.POST.get('userId')
    record_id = request.POST.get('recordId')
    print(record_id)
    upload_dir = os.path.join(BASE_DIR, 'upload', 'user_upload', 'user_%s' % user_id)
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        upload_path = os.path.join(upload_dir, fileObj.name)
        # try:
        #     with open(upload_path, mode='rb') as f:
        #         pass
        # except FileNotFoundError:
        #     with open(upload_path, mode='wb') as f:
        #         print("文件创建成功！")

    f = open(upload_path, 'wb')
    for chunk in fileObj.chunks():
        f.write(chunk)
        f.close()

    # The reason for this error is that .get() returns an individual object and.update() only works on querysets, such as what would be returned with .filter() instead of .get().
    ExerRecord.objects.filter(pk=record_id).update(uploadStatus=True, uploadTime=datetime.datetime.now(), uploadFilename=fileObj.name)
    # print(type(record))
    # record.save()

    return JsonResponse({'msg': 'upload successfully!'})


# 帖子展示 ######################################################################

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


def get_tag_list(request):
    # 获取每类标签的帖子的数量
    tag_list = []
    num = 0
    TagSet = PostTag.objects.all()
    for t in TagSet:  # 直接遍历QuerySet
        # Post模型中的postTag是外键,不是数据字符串
        try:
            p = Post.objects.filter(postTag=t)
            num = len(p)
        except p.DoesNotExist: # 没有该tag的帖子
            num = 0
            # print(num)
        tag_list.append({"tagName": str(t), "tagNum": num})

    return JsonResponse(json.dumps(tag_list), safe=False)


def get_post_list(request):
    # 获取post列表的相关信息
    post_list = []
    post = Post.objects.all()
    for p in post:
        post_list.append({
            'post_id': p.id,
            'poster': p.postPerson.userName,
            'post_title': p.postTitle,
            'post_tag': p.postTag.postTag,
            'post_create_time': p.postCreateTime,
            'post_modify_time': p.postModifyTime,
            'reply_num': len(p.postReply.all()),
            'view_num': p.postViewNum
        })

    return JsonResponse(json.dumps(post_list, cls=ComplexEncoder), safe=False)


def get_tag_post(request):
    # 获取每一类的帖子对象
    req = json.loads(request.body.decode())
    tag_name = req["tag_name"]
    post_list = []
    post = Post.objects.filter(postTag=PostTag.objects.get(postTag=tag_name))
    for p in post:
        post_list.append({
            'post_id': p.id,
            'poster': p.postPerson.userName,
            'post_title': p.postTitle,
            'post_tag': p.postTag.postTag,
            'post_create_time': p.postCreateTime,
            'post_modify_time': p.postModifyTime,
            'reply_num': len(p.postReply.all()),
            'view_num': p.postViewNum
        })

    return JsonResponse(json.dumps(post_list, cls=ComplexEncoder), safe=False)


# 帖子回复 ###########################################################

def get_reply(request):
    reply_list = []
    req = json.loads(request.body.decode())
    post_id = req["post_id"]  # 不能和模型字段名一样，会报错
    msg = ""

    post = Post.objects.get(pk=post_id)
    num = post.postViewNum+1
    Post.objects.filter(pk=post_id).update(postViewNum=num)
    postObj = {
        'poster': post.postPerson.userName,
        'post_title': post.postTitle,
        'post_content': post.postContent,
        'post_tag': post.postTag.postTag,
        'post_create_time': post.postCreateTime,
        'post_modify_time': post.postModifyTime,
        'reply_num': len(post.postReply.all()),
        'view_num': post.postViewNum,
    }
    reply_list.append(postObj)

    try:
        reply = post.postReply.all()
    except reply.DoesNotExist:
        msg = "该帖子尚无回复！"
    else:
        msg = "有回复"
        for r in reply:
            reply_list.append({
                "reply_from": r.replyFrom.userName,
                "reply_to": r.replyTo.userName,
                "reply_content": r.replyContent,
                "reply_time": r.replyTime,
                "msg": msg
            })

    return JsonResponse(json.dumps(reply_list, cls=ComplexEncoder), safe=False)


def create_post_reply(request):
    req = json.loads(request.body.decode())
    reply_from = req["reply_from"]
    reply_to = req["reply_to"]
    reply_content = req["reply_content"]
    reply_post = req["reply_post"]
    post_reply = PostReply.objects.create(
        replyFrom=User.objects.get(pk=reply_from),
        replyTo=User.objects.get(userName=reply_to),
        replyContent=reply_content
    )
    Post.objects.get(pk=reply_post).postReply.add(post_reply)
    # 写入post的活动时间
    Post.objects.filter(pk=reply_post).update(postModifyTime=datetime.datetime.now())

    return JsonResponse({"msg": "回复成功！"})


def create_reply_reply(request):
    req = json.loads(request.body.decode())
    reply_from = req["reply_from"]
    reply_to = req["reply_to"]
    reply_content = req["reply_content"]
    reply_post = req["reply_post"]
    post_reply = PostReply.objects.create(
        replyFrom=User.objects.get(pk=reply_from),
        replyTo=User.objects.get(userName=reply_to),
        replyContent=reply_content
    )
    Post.objects.get(pk=reply_post).postReply.add(post_reply)
    # 写入post的活动时间
    Post.objects.filter(pk=reply_post).update(postModifyTime=datetime.datetime.now())

    return JsonResponse({"msg": "回复成功！"})


# 个人记录 #################################################################

def get_quiz_record(request):
    req = json.loads(request.body.decode())
    recordList = []
    # 当用户退出登录时，会产生异常
    try:
        userName = req["username"]
    except BaseException:
        return JsonResponse(json.dumps(recordList), safe=False)

    recordSet = ExerRecord.objects.filter(user=User.objects.get(userName=userName))
    for r in recordSet:
        recordList.append({
            'quiz_id': r.quiz.quizId,
            'quiz_text': r.quiz.quizText,
            'quiz_type': r.quiz.quizType.quizTypeName,
            'download_time': r.downloadTime,
            'upload_status': r.uploadStatus,
            'quiz_score': r.quizScore,
            'result_info': r.resultInfo,
            'upload_time': r.uploadTime,
            'correct_status': r.correctStatus,
            'record_id': r.id,
        })

    return JsonResponse(json.dumps(recordList, cls=ComplexEncoder), safe=False)


def get_post_record(request):
    req = json.loads(request.body.decode())
    recordList = []
    # 当用户退出登录时，会产生异常
    try:
        userName = req["username"]
    except BaseException:
        return JsonResponse(json.dumps(recordList), safe=False)

    recordSet = Post.objects.filter(postPerson=User.objects.get(userName=userName))
    for r in recordSet:
        recordList.append({
            'post_id': r.id,
            'poster': r.postPerson.userName,
            'post_title': r.postTitle,
            'post_tag': r.postTag.postTag,
            'post_create_time': r.postCreateTime,
            'post_modify_time': r.postModifyTime,
            'reply_num': len(r.postReply.all()),
            'view_num': r.postViewNum,
        })

    return JsonResponse(json.dumps(recordList, cls=ComplexEncoder), safe=False)


# 模拟批阅 #################################################################

def correct_quiz(request):
    req = json.loads(request.body.decode())
    record_id = req["record_id"]
    quiz_score = req["quiz_score"]
    correct_info = req["correct_info"]

    ExerRecord.objects.filter(pk=record_id).update(quizScore=quiz_score, resultInfo=correct_info, correctTime=datetime.datetime.now(), correctStatus=True)

    return JsonResponse({"msg": "批阅成功！"})
