from django.urls import path
from .views import squat_view, video_feed, stop_stream, result_page, overall_result_page

urlpatterns = [
    path('suqat/', squat_view, name='squat'),
    path('video_feed/', video_feed, name='video_feed_squat'),
    path('stop_stream/', stop_stream, name='squat_stop_stream'),
    path('result/', result_page, name='squat_result'),
    path('overall_result/', overall_result_page, name='user_squat_result'),
]