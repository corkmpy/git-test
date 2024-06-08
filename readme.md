# health Keeper 1

개요

*사용기술* 
Python 기반 웹 프레임워크인 Django를 사용하였고, 
DBMS는 Django에서 기본으로 제공하는 SQLite를 사용하였습니다. 
카메라를 활용하는 model은 mediapipe를 사용하였습니다.

*사용 방법*

pip install Package               Version
--------------------- -----------
absl-py               2.1.0
asgiref               3.8.1
attrs                 23.2.0
certifi               2024.2.2
cffi                  1.16.0
charset-normalizer    3.3.2
contourpy             1.2.1
cycler                0.12.1
Django                5.0.6
djangorestframework   3.15.1
flatbuffers           24.3.25
fonttools             4.51.0
idna                  3.7
jax                   0.4.28
jaxlib                0.4.28
kiwisolver            1.4.5
matplotlib            3.8.4
mediapipe             0.10.14
ml-dtypes             0.4.0
numpy                 1.26.4
opencv-contrib-python 4.9.0.80
opencv-python         4.9.0.80
opt-einsum            3.3.0
packaging             24.0
pillow                10.3.0
pip                   24.0
protobuf              4.25.3
pycparser             2.22
pyparsing             3.1.2
python-dateutil       2.9.0.post0
requests              2.31.0
scipy                 1.13.0
six                   1.16.0
sounddevice           0.4.6
sqlparse              0.5.0
tzdata                2024.1
urllib3               2.2.1
channels


*개발 배경*

집에서 운동하는 인구수의 증가로 인한 케어방식에 대한 고민으로, AI가 웹캠 또는 스마트폰카메라를 이용해 운동을 교정해주는 프로그램을 개발하고 싶었습니다.

*사용 시나리오*

회원가입 후 > 교정버튼을 눌러 운동 3가지(추후 늘려갈 예정) 선택을 하고, 사용자의 신체 의 각도가 일정 각도가 될 경우에 count를 올라가게 하고, plank의 경우 사용자가 미리 지정한 운동시간이 지날경우 결과페이지로 넘어갑니다.
사용자의 운동 욕구를 증가시키기 위하여 랭킹시스템을 도입하여, 다른 사용자들간의 경쟁 심리를 부추기려 했습니다.

설계 및 구현

cpu 환경에서 작업할수 있도록 opencv-pose 대신 mediapipe를 활용하여 고정된 이미지에서 각도를 가져와 사용자의 신체각도와 비교후 유사도 범위를 정하여 일치할경우 count가 올라갈수있게 작업하였습니다.

