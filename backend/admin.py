# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from backend.models import User
from backend.models import QuizBank, QuizType, KnowledgePoint, QuizKnowledgePointShip
from backend.models import ExerRecord


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
    # fields = (
    #     'quizId', 'quizInputer', 'quizType',
    #     'quizText', 'quizPointNum',
    #     'quizFullScore', 'quizFilename'
    # )
    # filter_horizontal = ('quizKnowledgePoint',)


class QuizKnowledgePointShipAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'knowledgePoint')


class ExerRecordAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'quiz',
        'resultInfo', 'quizScore',
        'uploadFilename'
    )
    fields = ('user', 'quiz', 'resultInfo', 'quizScore', 'uploadFilename')


admin.site.register(User, UserAdmin)
admin.site.register(QuizBank, QuizBankAdmin)
admin.site.register(ExerRecord, ExerRecordAdmin)
admin.site.register(QuizType, QuizTypeAdmin)
admin.site.register(KnowledgePoint, KnowledgePointAdmin)
admin.site.register(QuizKnowledgePointShip, QuizKnowledgePointShipAdmin)
