from django.urls import path
from . import views
app_name = 'backend'


urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('get_quiz/', views.get_quiz),
    path('download/', views.download),
    path('get_quiz_record/', views.get_quiz_record),
    path('get_post_record/', views.get_post_record),
    path('upload/', views.upload),
    path('create_post/', views.create_post),
    path('get_post_list/', views.get_post_list),
    path('get_tag_list/', views.get_tag_list),
    path('get_reply/', views.get_reply),
    path('create_post_reply/', views.create_post_reply),
    path('create_reply_reply/', views.create_reply_reply),
    path('correct_quiz/', views.correct_quiz)
]
