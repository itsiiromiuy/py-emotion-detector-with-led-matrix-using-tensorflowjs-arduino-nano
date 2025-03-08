import cv2
import mediapipe as mp

# from pinpong.board import NeoPixel
# from pinpong.board import Board
# from pinpong.board import Pin
# from pinpong.board import PWM
# import time

# 初始化单片机板和NeoPixel
# Board("uno").begin()
# pin1 = Pin(Pin.D5, Pin.PWM)
# np = NeoPixel(pin1, 64)
# pwm = PWM(Pin(Pin.D5))

# # 检测硬件
# for index in range(5):
#     np.rainbow(0, 63, 1, 360)
#     time.sleep(0.3)
#     np.clear()
#     time.sleep(0.3)


# Replace np.clear() and np[i] with print statements:

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

# I wanna flip the camera
 

# 需要检测的关键点索引
key_points = [291, 13, 14, 61, 385, 387, 380, 373, 160, 144, 158, 153]

# 判断是否为微笑
def is_smiling(face_landmarks):
    return face_landmarks.landmark[291].y < face_landmarks.landmark[13].y and \
           face_landmarks.landmark[61].y < face_landmarks.landmark[13].y

# 判断是否为悲伤
def is_sad(face_landmarks):
    return face_landmarks.landmark[291].y > face_landmarks.landmark[14].y and \
           face_landmarks.landmark[61].y > face_landmarks.landmark[14].y

# 判断是否为大笑
def is_laughing(face_landmarks):
    return (face_landmarks.landmark[291].x - face_landmarks.landmark[61].x) < \
           (face_landmarks.landmark[14].y - face_landmarks.landmark[13].y)

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
        for face_landmarks in results.multi_face_landmarks:
            # 绘制检测到的关键点
            for idx in key_points:
                landmark = face_landmarks.landmark[idx]
                x, y = int(landmark.x * width), int(landmark.y * height)
                cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

            # 判断表情并控制NeoPixel灯条
            if is_smiling(face_landmarks):
                text = "Smiling"
                cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                # np.clear()
                # # 笑容灯光特效
                # nums = [17, 13, 19, 21, 9, 23, 34, 44, 43, 37]
                # for i in nums:
                #     np[i] = (0, 255, 0)

            elif is_sad(face_landmarks):
                text = "Sad"
                cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
             
            #     np.clear()
            #     # 悲伤灯光特效
            #     nums = [17, 18, 19, 21, 23, 45, 35, 36, 42]
            #     for i in nums:
            #         np[i] = (0, 255, 0)

            elif is_laughing(face_landmarks):
                text = "Laughing"
                cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            #     np.clear()
            #     # 大笑灯光特效
            #     nums = [17, 13, 19, 21, 9, 23, 33, 45, 44, 43, 42, 38, 35, 36]
            #     for i in nums:
            #         np[i] = (255, 255, 0)

    # 显示图像

    flipped_frame = cv2.flip(image, 1)
    cv2.imshow('Face Mesh', flipped_frame)


    # 退出'q'键检测
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头和窗口
cap.release()
cv2.destroyAllWindows
