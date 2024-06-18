import math
import cv2
import numpy as np
from time import time
import mediapipe as mp
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
from accounts.models import CustomUser 
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from collections import defaultdict
from django.utils.timezone import localtime

#랭킹 시스템을 위해
from django.db.models import Avg
# 데이터 저장을 위해
from .models import Squat_data
# mediapipe pose 클래스 초기화
mp_pose = mp.solutions.pose

# Pose 기능 설정
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)

# mediapipe drawing 클래스 초기화
mp_drawing = mp.solutions.drawing_utils

# 포즈 추적을 위한 전역 변수 초기화
count = 0
prev_label = 'incorrect pose'
max_similarity = {'left_elbow': 0, 'right_elbow': 0, 'left_knee': 0, 'right_knee': 0, 'waist': 0}  # 가장 높은 유사도 초기값

# 이미지 불러오기
image_path = os.path.join(settings.BASE_DIR, 'static/images/SquatPose.jpg')
if not os.path.exists(image_path):
    raise FileNotFoundError(f"Image not found at {image_path}")

image = cv2.imread(image_path)
if image is None:
    raise ValueError("Image could not be loaded, check the path and file format.")
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results1 = pose.process(image_rgb)
landmarks2 = []
if results1.pose_landmarks:
    for landmark in results1.pose_landmarks.landmark:
        landmarks2.append((landmark.x, landmark.y, landmark.z))

# 유사도를 구하는 함수
def calculateAngleSimilarity(angle1, angle2):
    # 각도의 코사인 값을 계산
    cos_angle1 = math.cos(math.radians(angle1))
    cos_angle2 = math.cos(math.radians(angle2))

    # 코사인 유사도를 계산합니다.
    similarity = (cos_angle1 * cos_angle2 + 1) / 2  # [0, 1] 범위로 정규화한다.

    # 유사도를 퍼센트로 변환하여 [0, 100] 범위로 표시합니다.
    similarity_percent = similarity * 100
    return similarity_percent

# 각도를 계산 함수
def calculateAngle(landmark1, landmark2, landmark3):
    if 0 in (landmark1, landmark2, landmark3):
        return 0
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    if angle < 0:
        angle += 360
    return angle

# 참조 이미지의 각도 계산

left_elbow_angle2 = calculateAngle(landmarks2[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                   landmarks2[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                   landmarks2[mp_pose.PoseLandmark.LEFT_WRIST.value])
right_elbow_angle2 = calculateAngle(landmarks2[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                    landmarks2[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                    landmarks2[mp_pose.PoseLandmark.RIGHT_WRIST.value])

left_knee_angle2 = calculateAngle(landmarks2[mp_pose.PoseLandmark.LEFT_HIP.value],
                                  landmarks2[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                  landmarks2[mp_pose.PoseLandmark.LEFT_ANKLE.value])
right_knee_angle2 = calculateAngle(landmarks2[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                   landmarks2[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                   landmarks2[mp_pose.PoseLandmark.RIGHT_ANKLE.value])

waist_angle2 = calculateAngle(landmarks2[mp_pose.PoseLandmark.LEFT_HIP.value],
                              landmarks2[mp_pose.PoseLandmark.RIGHT_HIP.value],
                              landmarks2[mp_pose.PoseLandmark.NOSE.value])
# 자세 분류 함수
def classifyPose(landmarks, output_image, display=False):
    global count, prev_label, max_similarity
    label = 'incorrect pose'
    color = (0, 0, 255)
    
    # 유사도를 저장할 딕셔너리
    similarities = {}
    
    # 이미지와 영상의 관절 각도 유사도 계산 및 딕셔너리에 저장
    left_elbow_angle = calculateAngle(
        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
    if left_elbow_angle != 0:
        left_elbow_similarity = calculateAngleSimilarity(left_elbow_angle2, left_elbow_angle)
        similarities['left_elbow'] = left_elbow_similarity
    else:
        similarities['left_elbow'] = 0  # 0 또는 적절한 기본값

    right_elbow_angle = calculateAngle(
        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])
    if right_elbow_angle != 0:
        right_elbow_similarity = calculateAngleSimilarity(right_elbow_angle2, right_elbow_angle)
        similarities['right_elbow'] = right_elbow_similarity
    else:
        similarities['right_elbow'] = 0

    left_knee_angle = calculateAngle(
        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
        landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
        landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])
    if left_knee_angle != 0:
        left_knee_similarity = calculateAngleSimilarity(left_knee_angle2, left_knee_angle)
        similarities['left_knee'] = left_knee_similarity
    else:
        similarities['left_knee'] = 0

    right_knee_angle = calculateAngle(
        landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
        landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])
    if right_knee_angle != 0:
        right_knee_similarity = calculateAngleSimilarity(right_knee_angle2, right_knee_angle)
        similarities['right_knee'] = right_knee_similarity
    else:
        similarities['right_knee'] = 0

    waist_angle = calculateAngle(
        landmarks2[mp_pose.PoseLandmark.LEFT_HIP.value],
        landmarks2[mp_pose.PoseLandmark.RIGHT_HIP.value],
        landmarks2[mp_pose.PoseLandmark.NOSE.value])
    if waist_angle != 0:
        waist_similarity = calculateAngleSimilarity(waist_angle2, waist_angle)
        similarities['waist'] = waist_similarity
    else:
        similarities['waist'] = 0
    # 가장 높은 유사도 갱신
    for joint, similarity in similarities.items():
        max_similarity[joint] = max(max_similarity[joint], similarity)
    
    # 'Accurate pose'인 경우
    if similarities['left_elbow'] > 75 and similarities['right_elbow'] > 75:
        if similarities['left_knee'] > 50 and similarities['right_knee'] > 50 and similarities['waist'] > 50:  # 임계값 조정 가능
            label = 'Accurate pose'
            color = (0, 255, 0)
            if prev_label == 'incorrect pose':
                count += 1
    prev_label = label
    
    
    if display:
        plt.figure(figsize=[10,10])
        plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off')
    else:
        return output_image, label
    
# 자세 검출 함수
def detectPose(image, pose, display=True):
    output_image = image.copy()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(imageRGB)
    height, width, _ = image.shape
    landmarks = []

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks, connections=mp_pose.POSE_CONNECTIONS)
        for landmark in results.pose_landmarks.landmark:
            # 랜드마크의 화면 내 위치를 확인
            if 0 <= landmark.x <= 1 and 0 <= landmark.y <= 1:
                landmarks.append((int(landmark.x * width), int(landmark.y * height), (landmark.z * width)))
            else:
                # 화면 밖에 있는 랜드마크는 (0, 0, 0)으로 표시
                landmarks.append((0, 0, 0))

        return output_image, landmarks

    return output_image, landmarks

pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)

camera = cv2.VideoCapture(0)
 
# 웹캠 스트림 생성 함수
def gen(camera):
   
    global count_final, similarities
    time1 = 0
    while True:
        ok, frame = camera.read()
        if not ok:
            continue
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ =  frame.shape
        frame = cv2.resize(frame, (int(frame_width * (640 / frame_height)), 640))
        frame, landmarks_video = detectPose(frame, pose_video, display=False)
        time2 = time()
        time1 = time2
    
        if landmarks_video and len(landmarks_video) == 33:
            # 이미지와 영상의 관절 각도 유사도 계산
            left_elbow_similarity = calculateAngleSimilarity(left_elbow_angle2, calculateAngle(
                landmarks_video[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                landmarks_video[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                landmarks_video[mp_pose.PoseLandmark.LEFT_WRIST.value]))
        
            right_elbow_similarity = calculateAngleSimilarity(right_elbow_angle2, calculateAngle(
                landmarks_video[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                landmarks_video[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                landmarks_video[mp_pose.PoseLandmark.RIGHT_WRIST.value]))

            left_knee_similarity = calculateAngleSimilarity(left_knee_angle2, calculateAngle(
                landmarks_video[mp_pose.PoseLandmark.LEFT_HIP.value],
                landmarks_video[mp_pose.PoseLandmark.LEFT_KNEE.value],
                landmarks_video[mp_pose.PoseLandmark.LEFT_ANKLE.value]))

            right_knee_similarity = calculateAngleSimilarity(right_knee_angle2, calculateAngle(
                landmarks_video[mp_pose.PoseLandmark.RIGHT_HIP.value],
                landmarks_video[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                landmarks_video[mp_pose.PoseLandmark.RIGHT_ANKLE.value]))
        
            waist_similarity = calculateAngleSimilarity(waist_angle2, calculateAngle(
                landmarks_video[mp_pose.PoseLandmark.LEFT_HIP.value],
                landmarks_video[mp_pose.PoseLandmark.RIGHT_HIP.value],
                landmarks_video[mp_pose.PoseLandmark.NOSE.value]))
            # 각도 유사도를 이미지 왼쪽 상단에 추가
            cv2.putText(frame, f"Left Elbow Similarity: {left_elbow_similarity:.2f}%", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
            cv2.putText(frame, f"Right Elbow Similarity: {right_elbow_similarity:.2f}%", (10, 90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
            cv2.putText(frame, f"Left Knee Similarity: {left_knee_similarity:.2f}%", (10, 120), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
            cv2.putText(frame, f"Right Knee Similarity: {right_knee_similarity:.2f}%", (10, 150), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
            cv2.putText(frame, f"Waist Similarity: {waist_similarity:.2f}%", (10, 180), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        
        if landmarks_video:
            frame, _ = classifyPose(landmarks_video, frame, display=False)
        
        cv2.putText(frame, f'Count: {count}', (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        _, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
        # 여기에서 average_similarity를 계산
        for joint, similarity in max_similarity.items():
            similarities.append(similarity)
            average_similarity = sum(similarities) / len(similarities)  
        count_final = count
    
#저장을 위한 전역 변수 설정
average_similarity = 0
count_final = 0
User = get_user_model()
similarities = []
#스트림 종료시 실행되는 함수, 데이터도 저장함
def cleanup(user):
    global average_similarity, count_final, similarities

    if similarities:
        average_similarity = sum(similarities) / len(similarities)
    # 모델에 데이터 저장
    Squat_data.objects.create(
        user = user,
        average_similarity=average_similarity,
        count_final=count_final
    )

def video_feed(request):
    return StreamingHttpResponse(gen(camera),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def squat_view(request):
    return render(request, 'squat/squat.html')

@login_required
def stop_stream(request):
    if request.method == 'POST':
        user = request.user
        
        cleanup(user)  # 스트림 종료 시 cleanup 호출

        # cleanup 후에 저장된 데이터를 가져오기
        latest_data = Squat_data.objects.filter(user=user).order_by('-timestamp').first()
        
        return JsonResponse({'status': 'success', 'count_final': latest_data.count_final, 'average_similarity': latest_data.average_similarity})
    return JsonResponse({'status': 'error'})

@login_required
def result_page(request):
    user = request.user
    latest_data = Squat_data.objects.filter(user=user).order_by('-timestamp').first()
    context = {
        'user': user,
        'count_final': latest_data.count_final,
        'average_similarity': latest_data.average_similarity,
    }
    return render(request, 'squat/squat_result.html', context)

#랭킹을 위해서
@login_required
def overall_result_page(request):
    user = request.user
    exercise_sessions = Squat_data.objects.filter(user=user).order_by('-timestamp')
    total_sessions = exercise_sessions.count()
    total_counts = sum(session.count_final for session in exercise_sessions)
    
    # 전체 사용자 유사도 랭킹 데이터 가져오기
    users_ranking = User.objects.annotate(average_similarity=Avg('squat_data__average_similarity')).order_by('-average_similarity')
    
    context = {
        'user': user,
        'total_sessions': total_sessions,
        'total_counts': total_counts,
        'exercise_sessions': exercise_sessions,
        'users_ranking': users_ranking,
    }
    return render(request, 'squat/user_squat_resutl.html', context)

