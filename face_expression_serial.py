import cv2
import mediapipe as mp
import time
import multiprocessing
from pinpong.board import NeoPixel, Board, Pin, PWM

def arduino_worker(shared_expression):
    board = Board("uno", port="/dev/cu.usbserial-57860561021")  
    board.begin()
    pin1 = Pin(Pin.D9, Pin.PWM)
    np = NeoPixel(pin1, 64)
    pwm = PWM(Pin(Pin.D9))

    last_expression = ""  

    while True:
        expression = shared_expression.value  
        if expression != last_expression: 
            np.clear()
            if expression == "Smiling":
                nums = [10, 13, 18, 21, 33, 38, 41, 46, 50, 51, 52, 53]
                for i in nums:
                    np[i] = (0, 255, 0)  
            elif expression == "Neutral":
                nums = [17, 18, 21, 22, 41, 42, 43, 44, 45, 46]
                for i in nums:
                    np[i] = (0, 0, 255)   
            elif expression == "Angry":
                nums = [10, 13, 18, 21, 34, 35, 36, 37, 41, 46, 49, 54]
                for i in nums:
                    np[i] = (255, 0, 0)  

            last_expression = expression  

        time.sleep(0.1)  

def is_smiling(face_landmarks):
    return face_landmarks.landmark[291].y < face_landmarks.landmark[13].y and \
           face_landmarks.landmark[61].y < face_landmarks.landmark[13].y

def is_neutral(face_landmarks):
 
    horizontal_distance = abs(face_landmarks.landmark[33].x - face_landmarks.landmark[159].x)
    vertical_distance = abs(face_landmarks.landmark[130].y - face_landmarks.landmark[243].y)
    return horizontal_distance < vertical_distance

def is_angry(face_landmarks):
    # TODO: 
    vertical_compression = abs(face_landmarks.landmark[33].y - face_landmarks.landmark[159].y)
    normal_brow_height = abs(face_landmarks.landmark[130].y - face_landmarks.landmark[243].y)
    return vertical_compression < normal_brow_height


def main():

    mp_drawing = mp.solutions.drawing_utils
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh()

    cap = cv2.VideoCapture(0)
    # TODO: refine key points
    key_points = [291, 13, 14, 61, 385, 387, 380, 373, 160, 144, 158, 153]

    shared_expression = multiprocessing.Manager().Value('u', "Neutral")  

    arduino_process = multiprocessing.Process(target=arduino_worker, args=(shared_expression,))
    arduino_process.daemon = True   
    arduino_process.start()

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, _ = image.shape

        results = face_mesh.process(image_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for idx in key_points:
                    landmark = face_landmarks.landmark[idx]
                    x, y = int(landmark.x * width), int(landmark.y * height)
                    cv2.circle(image, (x, y), 2, (0, 255, 0), -1)   

                if is_smiling(face_landmarks):
                    shared_expression.value = "Smiling"      
                elif is_angry(face_landmarks):
                    shared_expression.value = "Angry"
                elif is_neutral(face_landmarks):
                    shared_expression.value = "Neutral"

                cv2.putText(image, shared_expression.value, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        flipped_frame = cv2.flip(image, 1)

        cv2.imshow('Face Mesh', flipped_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    arduino_process.terminate()  
    arduino_process.join()


if __name__ == "__main__":
    main()
