from django.urls import path
from . import views
app_name = 'backend'


urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('get_quiz/', views.get_quiz),
    path('get_type_list/', views.get_type_list),
    path('get_type_quiz/', views.get_type_quiz),
    path('get_point_quiz/', views.get_point_quiz),
    path('get_knowledge_point/', views.get_knowledge_point),
    path('download/', views.download),
    path('get_quiz_record/', views.get_quiz_record),
    path('get_post_record/', views.get_post_record),
    path('get_collect_record/', views.get_collect_record),
    path('upload/', views.upload),
    path('create_post/', views.create_post),
    path('get_post_list/', views.get_post_list),
    path('get_tag_post/', views.get_tag_post),
    path('get_tag_list/', views.get_tag_list),
    path('get_reply/', views.get_reply),
    path('create_post_reply/', views.create_post_reply),
    path('create_reply_reply/', views.create_reply_reply),
    path('collect_post/', views.collect_post),
    path('correct_quiz/', views.correct_quiz)
]
