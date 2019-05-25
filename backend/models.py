# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import django.contrib.auth.models as admin
from django.utils import timezone


class User(models.Model):
    userName = models.CharField(max_length=12, verbose_name="用户名")
    userPasswd = models.CharField(max_length=20, verbose_name="密码")
    registerTime = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")

    class Meta:
        db_table = 'user_info'
        verbose_name = '用户管理'
        verbose_name_plural = '1-0. 用户管理'

    def __str__(self):
        return self.userName


class QuizType(models.Model):
    quizTypeId = models.CharField(
        max_length=2,
        primary_key=True,
        verbose_name="试题分类编号"
    )
    quizTypeName = models.CharField(max_length=10, verbose_name="试题分类")

    class Meta:
        db_table = 'quiz_type'
        verbose_name = '题型管理'
        verbose_name_plural = '2-2. 题型管理'

    def __str__(self):
        return u'%s' % (self.quizTypeName)


class KnowledgePoint(models.Model):
    quizType = models.ForeignKey(
        QuizType,
        on_delete=models.CASCADE,
        verbose_name="试题分类"
    )
    knowledgePointId = models.CharField(
        primary_key=True,
        max_length=4,
        verbose_name="知识点编号"
    )
    knowledgePoint = models.CharField(max_length=15, verbose_name="知识点")

    class Meta:
        db_table = 'knowledge_point'
        verbose_name = '知识点管理'
        verbose_name_plural = '2-1. 知识点管理'

    def __str__(self):
        return u'%s/%s' % (self.quizType, self.knowledgePoint)


class QuizBank(models.Model):
    POINT_NUM = (
        ('only', '单一'),
        ('many', '综合')
    )
    QUIZ_DIFFICULTY = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )
    quizId = models.CharField(max_length=20, verbose_name="试题编号")
    quizType = models.ForeignKey(
        QuizType,
        on_delete=models.CASCADE,
        verbose_name="试题分类"
    )
    quizPointNum = models.CharField(
        max_length=4,
        choices=POINT_NUM,
        verbose_name="知识点数"
    )
    quizKnowledgePoint = models.ManyToManyField(
        KnowledgePoint,
        verbose_name="知识点"
    )
    quizText = models.TextField(max_length=1000, verbose_name="试题文本")
    quizFullScore = models.IntegerField(verbose_name="满分",)
    quizFilename = models.FileField(max_length=50, upload_to="%Y/%m/%d", verbose_name="文件名")
    quizDifficulty = models.CharField(
        max_length=1,
        choices=QUIZ_DIFFICULTY,
        verbose_name="难度系数"
    )
    quizInputer = models.ForeignKey(
        admin.User,
        on_delete=models.CASCADE,
        verbose_name="录题人"
    )
    quizCreateTime = models.DateTimeField(
        auto_now_add=True,
        verbose_name="录入时间"
    )
    quizModifyTime = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'quiz_bank'
        verbose_name = '题库管理'
        verbose_name_plural = '2-0. 题库管理'

    def __str__(self):
        return self.quizId


# class DownloadRecord(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name="用户"
#     )
#     quiz = models.ForeignKey(
#         QuizBank,
#         on_delete=models.CASCADE,
#         verbose_name="试题"
#     )
#     downloadTime = models.DateTimeField(auto_now_add=True, verbose_name="下载时间")

    
class ExerRecord(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="用户"
    )
    quiz = models.ForeignKey(
        QuizBank,
        on_delete=models.CASCADE,
        verbose_name="试题"
    )
    resultInfo = models.TextField(max_length=1000, null=True, verbose_name="批阅反馈")
    quizScore = models.IntegerField(null=True, verbose_name="得分")
    uploadFilename = models.CharField(null=True, max_length=20, verbose_name="文件名")
    uploadStatus = models.BooleanField(default=False, verbose_name="是否已上传")
    correctStatus = models.BooleanField(default=False, verbose_name="是否已批阅")
    downloadTime = models.DateTimeField(auto_now_add=True, verbose_name="下载时间")
    uploadTime = models.DateTimeField(null=True, verbose_name="上传时间")
    correctTime = models.DateTimeField(null=True, verbose_name="批阅时间")
    correctFlag = models.BooleanField(default=True, verbose_name="可否批阅")

    class Meta:
        db_table = 'exer_record'
        verbose_name = '练习管理'
        verbose_name_plural = '3-0. 练习管理'


class PostTag(models.Model):
    postTag = models.CharField(max_length=10, verbose_name="帖子标签名")
    tagCreateTime = models.DateTimeField(auto_now_add=True, verbose_name="标签创建时间")
    tagModifyTime = models.DateTimeField(auto_now=True, verbose_name="标签修改时间")

    class Meta:
        db_table = 'post_tag'
        verbose_name = '标签管理'
        verbose_name_plural = '4-2. 标签管理'

    def __str__(self):
        return self.postTag


class PostReply(models.Model):
    replyFrom = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="回复人",
        related_name='replyFrom'
    )
    replyTo = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="回复对象",
        related_name='replyTo'
    )
    replyContent = models.TextField(max_length=1000, verbose_name="回复内容")
    replyTime = models.DateTimeField(auto_now_add=True, verbose_name="回复时间")

    class Meta:
        db_table = 'post_reply'
        verbose_name = '回复管理'
        verbose_name_plural = '4-1. 回复管理'


class Post(models.Model):
    postTag = models.ForeignKey(
        PostTag,
        on_delete=models.CASCADE,
        verbose_name="帖子主题"
    )
    postTitle = models.CharField(max_length=100, verbose_name="帖子标题")
    postContent = models.TextField(max_length=1000, verbose_name="帖子内容")
    postPerson = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="发贴人"
    )
    postReply = models.ManyToManyField(
        PostReply,
        verbose_name="回复帖子",
        related_name="reply"
    )
    postCreateTime = models.DateTimeField(auto_now_add=True, verbose_name="发帖时间")
    postModifyTime = models.DateTimeField(default=timezone.now, verbose_name="修改时间")
    postViewNum = models.IntegerField(default=0, verbose_name="浏览量")
    stickyPost = models.BooleanField(default=False, verbose_name="是否置顶")

    class Meta:
        db_table = 'forum_post'
        verbose_name = '帖子管理'
        verbose_name_plural = '4-0. 帖子管理'
