# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from backend.models import User
from backend.models import QuizBank, QuizType, KnowledgePoint
from backend.models import ExerRecord
from backend.models import Post, PostReply, PostTag

import time
import datetime

class UserAdmin(admin.ModelAdmin):
    list_display = ('userName', 'userPasswd', 'registerTime')
    search_fields = ('userName',)


class QuizTypeAdmin(admin.ModelAdmin):
    list_display = ('quizTypeId', 'quizTypeName')
    ordering = ('quizTypeId',)


class KnowledgePointAdmin(admin.ModelAdmin):
    list_display = ('quizType', 'knowledgePointId', 'knowledgePoint')
    ordering = ('knowledgePointId',)


class QuizBankAdmin(admin.ModelAdmin):
    list_display = (
        'quizId', 'quizText','quizType', 'quizFullScore', 'quizInputer',
        'quizCreateTime', 'quizModifyTime'
    )
    fields = (
        'quizInputer','quizType',
        'quizText',
        'quizFullScore', 'quizDifficulty', 'quizPointNum',
        'quizKnowledgePoint', 'quizFilename',
    )
    list_filter = (
        'quizType', 'quizInputer',
        'quizCreateTime', 'quizModifyTime'
    )

    def save_model(self, request, obj, form, change):
        dbid = QuizBank.objects.last().id + 1
        quizid = str(obj.quizType)[0:1]
        if obj.quizPointNum == '单一':
            quizid += 's'
        else:
            quizid += 'c'
            # str += datetime.datetime.now().strftime('y%m%d%')
        quizid += obj.quizDifficulty
        quizid += '%04d' % dbid
        obj.quizId = quizid
        
        super().save_model(request, obj, form, change)


class ExerRecordAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'quiz', 'downloadTime',
        'uploadStatus', 'uploadFilename', 'uploadTime',
        'correctStatus', 'correctTime', 'correctFlag',
        'quizScore', 'resultInfo',
    )
    
    list_filter = (
        'user', 'quiz',
    )
    search_fields = ('user','quiz')
    

class PostAdmin(admin.ModelAdmin):
    list_display = (
        'postTitle', 'postContent', 'postPerson',
        'postTag', 'postViewNum', 
        'postCreateTime', 'postModifyTime'
    )


class PostReplyAdmin(admin.ModelAdmin):
    list_display = (
        'replyFrom', 'replyContent', 'replyTime'
    )


class PostTagAdmin(admin.ModelAdmin):
    list_display = ('postTag', 'tagCreateTime', 'tagModifyTime')


admin.site.register(User, UserAdmin)
admin.site.register(QuizBank, QuizBankAdmin)
admin.site.register(ExerRecord, ExerRecordAdmin)
admin.site.register(QuizType, QuizTypeAdmin)
admin.site.register(KnowledgePoint, KnowledgePointAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostReply, PostReplyAdmin)
admin.site.register(PostTag, PostTagAdmin)
