from django.urls import path
from website import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('getRegisterHS', views.getRegisterHS, name='getRegisterHS'),
    path('getRegisterPH', views.getRegisterPH, name='getRegisterPH'),
    path('postRegisterHS', views.postRegisterHS, name='postRegisterHS'),
    path('postRegisterPH', views.postRegisterPH, name='postRegisterPH'),

    path('gettrainning', views.gettrainning, name='gettrainning'),

    path('getdetect', views.getdetect, name='getdetect'),

    path('stream', views.stream_view, name="stream"),
    path('video_feed', views.video_feed, name="video-feed"),

    path('dsdd', views.dsdd, name="dsdd"),


    path('test', views.test, name="test"),
]
