from keras.models import load_model
import tensorflow as tf  # 학습된 모델을 불러오는데 사용
import numpy as np
import cv2  # 웹캠 불러오기와 영상처리에 사용
import speech_recognition as sr
from gtts import gTTS
import os
import time
import playsound
import keyboard

size = (224, 224)
# 웹캠 불러오기, 추가 설치된 웹캠을 사용하기위해 0을 1,2.. 변경
wepcam = cv2.VideoCapture(0)
# 웹캠 설정
wepcam.set(cv2.CAP_PROP_BUFFERSIZE, 5)

# 학습된 모델 불러오기
model = load_model("test_model.h5", compile=False)

# TTS로 음성 파일 생성
tts = gTTS(text = "마스크를 써주세요.", lang = "ko")
tts.save("Mask_off.mp3")

tts = gTTS(text = "마스크 착용을 확인했어요.", lang = "ko")
tts.save("Mask_on.mp3") 

while wepcam.isOpened():

    # 카메라로부터 프레임 값을 하나씩 읽음
    ret, frame = wepcam.read()
    # 위에서 읽기가 성공하면 true, 아니면 false를 ret에 저장
    if not ret:
        break
    
    # 모델의 프레임 사이즈를 조정
    model_f = cv2.resize(frame, size, frame)
    # 차원 확장과 값의 범위를 정규화  ??
    model_f = np.expand_dims(model_f, axis = 0) / 255.0
        
    # 예측단계
    is_on_prob = model.predict(model_f)[0]
    is_off_prob = model.predict(model_f)[1]
    is_mid_prob = model.predict(model_f)[2]
    # numpy.argmax는 다차원 배열이라면 차원의 가장 큰 값을 반환, 현재 0과 1을 반환
    is_on = np.argmax(is_on_prob)
    is_off = np.argmax(is_off_prob)
    is_mid = np.argmax(is_mid_prob)

     # 예측
    if is_off == 1:
        msg_mask = "Mask off"
        msg_mask += " ({:.1f})%".format(is_on_prob[is_on] * 100)

    elif is_on == 1:
        msg_mask = "Mask on"
        msg_mask += " ({:.1f})%".format(is_off_prob[is_off] * 100)

    elif is_mid == 1:
        msg_mask = "Mask Mid"
        msg_mask += " ({:.1f})%".format(is_mid_prob[is_mid] * 100)
    
    # 예측 문자열 출력
    cv2.putText(frame, msg_mask, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), thickness=2)

    cv2.imshow('face mask detection', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break    