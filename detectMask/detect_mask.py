# 1. 코드 정리, 최적화 필요

# load_model() 대신 tf.keras.models.load_model() 함수 사용하면 from keras.models import load_model 없어도 됌.
from keras.models import load_model
import numpy as np
import cv2
import sys
import time
import playsound
from gtts import gTTS
from pymata4 import pymata4
"""
import tensorflow as tf
import os
import keyboard
import speech_recognition as sr
"""

MODEL_CLASS_NUM = 3     # 클래스의 갯수
TRIG = 9                # 초음파 센서 trig 핀
ECHO = 10               # 초음파 센서 echo 핀
SERVO_PIN = 8           # 서보 모터 제어 핀
DISTANCE_CM = 2         # 인덱스
SERVO_CLOSE = 0         # 서보 모터 회전부를 바라보고 오른쪽(3시), 닫힘을 표현
SERVO_OPEN = 90         # 위쪽(12시), 열림을 표현

global isRun_sonar
global delay_cnt
global servo_state
path = './'  # 프로젝트 폴더
tts_text = ["마스크를 착용해주세요.", "마스크 착용을 확인했습니다.", "마스크를 옳바르게 착용해주세요."]
output_text = ["mask off", "mask on", "half mask"]
main_window = "face mask detection"          # 창 이름

size = (224, 224)                            # 구글 티처블 머신에서 224px 이미지로 학습
cap = cv2.VideoCapture(0)                    # 카메라 지정
cap.set(cv2.CAP_PROP_BUFFERSIZE, 50)         # 카메라 설정, 버퍼 사이즈 변경
model = load_model(filepath=path+'test_model.h5', compile=False)
msg_mask = ""

board = pymata4.Pymata4()

# 서보 모터
def servo(degree):
    global servo_state
    servo_state = degree

    # set the pin mode
    board.set_pin_mode_servo(SERVO_PIN)
    # set the servo to 0 degree
    board.servo_write(SERVO_PIN, degree)
    time.sleep(1)

def sonar_callback(data):
    global isRun_sonar
    global delay_cnt

    dist = data[DISTANCE_CM]

    if(0 < dist < 10):
        if isRun_sonar:
            print(dist)
            mask_notification(is_mask, msg_mask)
            isRun_sonar = False
        else:
            delay_cnt +=1

    if delay_cnt == 20:
        isRun_sonar = True
        delay_cnt = 0

def sonar(callback):
    global isRun_sonar
    global delay_cnt

    isRun_sonar = True
    delay_cnt = 0
    board.set_pin_mode_sonar(TRIG, ECHO, callback)
    print("sonar is called")
    
    try:
        time.sleep(.01)
        
    except KeyboardInterrupt:
        board.shutdown()
        sys.exit(0)

# 예측 정보에 대한 행동 실행
def mask_notification (label, str):
    global servo_state
    # 0: 미착용
    if label == 0:
        playsound.playsound('0.mp3', block=True)
        if servo_state != SERVO_CLOSE:
            servo(SERVO_CLOSE)     
    # 1: 착용
    elif label == 1:
        playsound.playsound('1.mp3', block=True) 
        if servo_state != SERVO_OPEN:
            servo(SERVO_OPEN)   
    # 2: 반
    else:
        playsound.playsound('2.mp3', block=True)
        if servo_state != SERVO_CLOSE:
            servo(SERVO_CLOSE)
    str = output_text[label]

# tts mp3파일 생성
def save_TTS(text, string): 
    tts = gTTS(text=text, lang='ko')
    filename = "{}.mp3".format(string)
    tts.save(filename) 

for i in range(MODEL_CLASS_NUM):
    save_TTS(tts_text[i], i)

sonar(sonar_callback)
servo(SERVO_CLOSE)
open_time = 0
isFirst = True

while cap.isOpened():
    if servo_state == SERVO_OPEN:
        if isFirst == True:
            open_time = time.time()
            isFirst = False

        elif (time.time() - open_time) > 5:
            servo(SERVO_CLOSE)
            isFirst = True

    start_t = time.time() 
    retval, frame = cap.read()      # 영상 정보 읽기 
    if not retval:
        break

    model_f = cv2.resize(frame, size, frame)
    model_f = np.expand_dims(model_f, axis = 0) / 255.0

    is_mask_probably = model.predict(model_f)[0]    # 각 클래스별로 정확도를 리스트로 반환
    is_mask = np.argmax(is_mask_probably)           # 입력받은 배열 중 가장 큰 값의 '인덱스'를 반환

    msg_mask += " ({:.1f})%".format(is_mask_probably[is_mask] * 100)  # 정확도
    cv2.putText(frame, output_text[is_mask], (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), thickness=2)

    end_t = time.time()
    fps = round(1./(end_t - start_t))
    cv2.putText(frame, str(fps), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 0, 0), thickness=2)

    cv2.imshow(main_window, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

board.shutdown()
cv2.destroyAllWindows()