import mediapipe
from mediapipe.tasks.python.vision import face_landmarker
import cv2

cap = cv2.VideoCapture(0)

landmarker = face_landmarker.FaceLandmarker()

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image.shape

    result = landmarker.detect_for_video(image_rgb)
    print(result)


    flipped_frame = cv2.flip(image, 1)
    cv2.imshow('Face Mesh', flipped_frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows