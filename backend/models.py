# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import django.contrib.auth.models as admin


class User(models.Model):
    userName = models.CharField(max_length=12, verbose_name="用户名")
    userPasswd = models.CharField(max_length=20, verbose_name="密码")

    class Meta:
        db_table = 'user_info'
        verbose_name = '用户信息'
        verbose_name_plural = '3. 用户信息'


class QuizType(models.Model):
    quizTypeId = models.CharField(
        max_length=2,
        primary_key=True,
        verbose_name="试题分类编号"
    )
    quizTypeName = models.CharField(max_length=10, verbose_name="试题分类")

    class Meta:
        db_table = 'quiz_type'
        verbose_name = '试题分类'
        verbose_name_plural = '4. 试题分类'

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
        verbose_name = '知识点'
        verbose_name_plural = '5. 知识点'

    def __str__(self):
        return u'%s/%s' % (self.quizType, self.knowledgePoint)


class QuizBank(models.Model):
    POINT_NUM = (
        ('only', '单一'),
        ('many', '综合')
    )
    quizId = models.CharField(primary_key=True, max_length=20)
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
        verbose_name="知识点",
        through='QuizKnowledgePointShip',
        through_fields=('quiz', 'knowledgePoint'),
    )
    quizText = models.TextField(max_length=1000, verbose_name="试题文本")
    quizFullScore = models.IntegerField(verbose_name="满分")
    quizFilename = models.FileField(upload_to="%Y/%m/%d", verbose_name="文件名")
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
        verbose_name = '题库'
        verbose_name_plural = '1. 题库'


class QuizKnowledgePointShip(models.Model):
    quiz = models.ForeignKey(
        QuizBank,
        on_delete=models.CASCADE,
        verbose_name="试题"
    )
    knowledgePoint = models.ForeignKey(
        KnowledgePoint,
        on_delete=models.CASCADE,
        verbose_name="知识点"
    )

    class Meta:
        db_table = 'quiz_knowledgePoint_ship'
        verbose_name = '试题知识点映射'
        verbose_name_plural = '6. 试题知识点映射'


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
    resultInfo = models.TextField(max_length=1000, verbose_name="批阅反馈")
    quizScore = models.IntegerField(verbose_name="得分")
    uploadFilename = models.CharField(max_length=20, verbose_name="文件名")
    uploadStatus = models.BooleanField(verbose_name="是否已上传")
    correctStatus = models.BooleanField(verbose_name="是否已批阅")
    downloadTime = models.DateTimeField(verbose_name="下载时间")
    uploadTime = models.DateTimeField(verbose_name="上传时间")
    correctTime = models.DateTimeField(verbose_name="批阅时间")
    correctFlag = models.BooleanField(verbose_name="可否批阅")

    class Meta:
        db_table = 'exer_record'
        verbose_name = '练习记录'
        verbose_name_plural = '2. 练习记录'
