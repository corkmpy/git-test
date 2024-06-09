from django.urls import path
from .views import pushup_view, video_feed, webcam, stop_stream, result_page, overall_result_page

urlpatterns = [
    path('',webcam , name = 'webcam'),
    path('pushup/', pushup_view, name='pushup'),
    path('video_feed/', video_feed, name='video_feed_pushup'),
    path('stop_stream/', stop_stream, name='pushup_stop_stream'),
    path('result/', result_page, name='pushup_result'),
    path('overall_result/', overall_result_page, name='user_pushup_result'),
   
]