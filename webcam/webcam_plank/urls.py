from django.urls import path
from .views import plank_view, video_feed, stop_stream, result_page, overall_result_page

urlpatterns = [
    path('plank/', plank_view, name='plank'),
    path('video_feed/', video_feed, name='video_feed_plank'),
    path('stop_stream/', stop_stream, name='plank_stop_stream'),
    path('result/', result_page, name='plank_result'),
    path('overall_result/', overall_result_page, name='user_plank_result'),
]