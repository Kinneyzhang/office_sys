# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from backend.models import User
from backend.models import QuizBank, QuizType, KnowledgePoint
from backend.models import ExerRecord
from backend.models import Post, PostReply, PostTag


class UserAdmin(admin.ModelAdmin):
    list_display = ('userName', 'userPasswd')
    search_fields = ('userName',)


class QuizTypeAdmin(admin.ModelAdmin):
    list_display = ('quizTypeId', 'quizTypeName')
    ordering = ('quizTypeId',)


class KnowledgePointAdmin(admin.ModelAdmin):
    list_display = ('quizType', 'knowledgePointId', 'knowledgePoint')
    ordering = ('knowledgePointId',)


class QuizBankAdmin(admin.ModelAdmin):
    list_display = (
        'quizType', 'quizInputer',
        'quizText', 'quizFullScore',
        'quizFilename', 'quizCreateTime',
        'quizModifyTime'
    )

    # def save_model(self, request, obj, form, change):
    #     quiztype = obj.quizType
    #     difficulty = obj.quizDifficulty
    #     quiz_id = '%sD%s0001' % (quiztype, difficulty)
    #     obj.objects.all().update(quizId=quiz_id)
    #     super().save_model(request, obj, form, change)


class ExerRecordAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'quiz', 'downloadTime',
        'uploadStatus', 'uploadFilename', 'uploadTime',
        'correctStatus', 'correctTime', 'correctFlag',
        'quizScore', 'resultInfo',
    )


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'postTag', 'postTitle',
        'postPerson', 'postCreateTime', 'postModifyTime'
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
