import cv2
import mediapipe as mp

from pinpong.board import NeoPixel
from pinpong.board import Board
from pinpong.board import Pin
from pinpong.board import PWM
import time


board = Board("uno", port="/dev/cu.usbserial-57860561021")  # Replace with your port
board.begin()
pin1 = Pin(Pin.D9, Pin.PWM)
np = NeoPixel(pin1, 64)
pwm = PWM(Pin(Pin.D9))


for index in range(5):
    np.rainbow(0, 63, 1, 360)
    time.sleep(0.3)
    np.clear()
    time.sleep(0.3)


# Replace np.clear() and np[i] with print statements:

def distance(landmarks, p1, p2):
    x1, y1 = landmarks.landmark[p1].x, landmarks.landmark[p1].y
    x2, y2 = landmarks.landmark[p2].x, landmarks.landmark[p2].y
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def calculate_left_ear(landmarks):
    left_ear = (distance(landmarks, 385, 380) + distance(landmarks, 387, 373)) / (2.0 * distance(landmarks, 362, 263))
    return left_ear

def calculate_right_ear(landmarks):
    right_ear = (distance(landmarks, 160, 144) + distance(landmarks, 158, 153)) / (2.0 * distance(landmarks, 33, 133))
    return right_ear

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh()


cap = cv2.VideoCapture(0)

 


key_points = [291, 13, 14, 61, 385, 387, 380, 373, 160, 144, 158, 153]
def is_smiling(face_landmarks):
    return face_landmarks.landmark[291].y < face_landmarks.landmark[13].y and \
           face_landmarks.landmark[61].y < face_landmarks.landmark[13].y

def is_sad(face_landmarks):
    return face_landmarks.landmark[291].y > face_landmarks.landmark[14].y and \
           face_landmarks.landmark[61].y > face_landmarks.landmark[14].y

def is_angry(face_landmarks):
    return (face_landmarks.landmark[33].x - face_landmarks.landmark[159].x) < \
           (face_landmarks.landmark[130].y - face_landmarks.landmark[243].y)


while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # 将图像转换为RGB格式
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image.shape

    # 使用FaceMesh模型进行人脸关键点检测
    results = face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        print(results)
        for face_landmarks in results.multi_face_landmarks:
            # 绘制检测到的关键点
            for idx in key_points:
                landmark = face_landmarks.landmark[idx]
                # print(face_landmarks)
                x, y = int(landmark.x * width), int(landmark.y * height)
                cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

            if is_smiling(face_landmarks):
                text = "Smiling"
                cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                np.clear()
                nums = [10, 13, 18, 21, 33, 38, 41, 46, 50,51,52,53]
                for i in nums:
                    np[i] = (0, 255, 0)

            elif is_sad(face_landmarks):
                text = "Sad"
                cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                np.clear()
                nums = [ 17, 18 ,21,22, 41, 42, 43, 44, 45,46]
                for i in nums:
                    np[i] = (0,0, 255)

            elif is_angry(face_landmarks):
                text = "Angry"
                cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                np.clear()
                nums = [10, 13, 18, 21, 34, 35, 36, 37, 41, 46, 49, 54]
                for i in nums:
                    np[i] = (255, 0, 0)  # Red for angry

    flipped_frame = cv2.flip(image, 1)
    cv2.imshow('Face Mesh', flipped_frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头和窗口
cap.release()
cv2.destroyAllWindows
