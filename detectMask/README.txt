### 군산대 IT정보제어공학과 2학년 2학기 정보제어 설계 입문 프로젝트
### 아두이노를 활용하는 프로젝트 진행

# 제목 : 마스크 확인기

### 목적
기본적으로 주어지는 아두이노, 서보모터, led, 초음파 센서 등을 이용하여 실용적인 장치를 만드는 것.
파이썬 환경에서 tensorflow, opencv와 간단하게 학습시킨 모델을 토대로 코로나 시대에 마스크를 착용했는지 확인하는 시스템을 만들고자 함.

### 개요
구글티처블 머신으로 마스크를 착용한 모습과 착용하지 않은 모습을 학습시킨 모델을 
파이썬 프로그래밍 언어로 착용 여부와 TTS 음성을 출력한다.

### 설치 방법
- 아두이노에 firmataExpress 1.2.0 업로드
- 파이썬 환경에 pymata4, numpy, playsound, opencv, gTTS 모듈 설치
- tensorflow 또는 keras 설치
  load_model() 대신 tf.keras.models.load_model() 함수 사용하면 from keras.models import load_model 없어도 됨.

### 실행 방법
sg90서보모터, HC-SR04 센서, 아두이노 UNO 사용
- TRIG, ECHO 상수는 센서 연결대로 수정
- SERVO_PIN 상수는 서보 연결대로 수정(가장 연한 선 = 제어 pin)

### 참고사항
fps:
    - https://learnopencv.com/how-to-find-frame-rate-or-frames-per-second-fps-in-opencv-python-cpp/
sonar:
    - https://github.com/MrYsLab/pymata-aio/issues/95
    - https://forum.arduino.cc/t/ultrasonic-sensor-hc-sr04-4-pins-control-through-python-arduino-command-api/226615
    - https://www.basic4mcu.com/bbs/board.php?bo_table=gac&wr_id=8914&sst=wr_hit&sod=desc&sop=and&page=187
auduino:
    - https://github.com/thearn/Python-Arduino-Command-API
pymata4:
    - https://github.com/MrYsLab/pymata4/blob/master/examples/hc-sr04_distance_sensor.py
