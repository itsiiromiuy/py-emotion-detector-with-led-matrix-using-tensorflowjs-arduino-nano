import cv2
import mediapipe as mp

from pinpong.board import NeoPixel
from pinpong.board import Board
from pinpong.board import Pin
from pinpong.board import PWM
import time

# 初始化单片机板和NeoPixel
Board("uno").begin()
pin1 = Pin(Pin.D5, Pin.PWM)
np = NeoPixel(pin1, 64)
pwm = PWM(Pin(Pin.D5))

# 检测硬件
for index in range(5):
    np.rainbow(0, 63, 1, 360)
    time.sleep(0.3)
    np.clear()
    time.sleep(0.3)

# 距离检测函数，返回两点间的距离数值
def distance(landmarks, p1, p2):
    x1, y1 = landmarks.landmark[p1].x, landmarks.landmark[p1].y
    x2, y2 = landmarks.landmark[p2].x, landmarks.landmark[p2].y
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

# 计算左眼的EAR，根据左眼的六个关键点
def calculate_left_ear(landmarks):
    left_ear = (distance(landmarks, 385, 380) + distance(landmarks, 387, 373)) / (2.0 * distance(landmarks, 362, 263))
    return left_ear

# 计算右眼的EAR，根据右眼的六个关键点
def calculate_right_ear(landmarks):
    right_ear = (distance(landmarks, 160, 144) + distance(landmarks, 158, 153)) / (2.0 * distance(landmarks, 33, 133))
    return right_ear

# 初始化Mediapipe的FaceMesh模型
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# 加载FaceMesh模型
face_mesh = mp_face_mesh.FaceMesh()

# 打开摄像头
cap = cv2.VideoCapture(0)

# 需要绘制的关键点索引
key_points = [291, 13, 14, 61, 385, 387, 380, 373, 160, 144, 158, 153]
