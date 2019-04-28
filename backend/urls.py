from django.urls import path
from . import views
app_name = 'backend'


urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('show_quiz/', views.show_quiz),
    path('download/', views.download),
    path('upload/', views.upload),
    path('create_post/', views.create_post),
    path('get_post/', views.get_post),
    path('get_tagNum/', views.get_tagNum),
]
