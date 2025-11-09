import cv2
from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

PAN_CHANNEL = 0
TILT_CHANNEL = 1

for ch in (PAN_CHANNEL, TILT_CHANNEL):
    kit.servo[ch].actuation_range = 180
    kit.servo[ch].set_pulse_width_range(500, 2500)

pan_angle = 90
tilt_angle = 90
kit.servo[PAN_CHANNEL].angle = pan_angle
kit.servo[TILT_CHANNEL].angle = tilt_angle

dispW = 1280
dispH = 720
flip = 2

gst_pipeline = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! \
          nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! \
          videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

center_x = dispW // 2
center_y = dispH // 2

face_cascade = cv2.CascadeClassifier("opencv/data/haarcascades/haarcascade_frontalface_default.xml")

PAN_STEP = 1       
TILT_STEP = 1
X_TOLERANCE = 30   
Y_TOLERANCE = 30

print("Starting...")

try:
    while True:
        ret, frame = cam.read()

        if not ret:
            print("Camera not detected")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(80, 80))

        if len(faces) > 0:
            (x, y, w, h) = max(faces, key=lambda f: f[2] * f[3])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            face_cx = x + w // 2
            face_cy = y + h // 2
            cv2.circle(frame, (face_cx, face_cy), 5, (0, 0, 255), -1)

            error_x = center_x - face_cx
            error_y = center_y - face_cy

            if abs(error_x) > X_TOLERANCE:
                if error_x > 0:
                    pan_angle += PAN_STEP
                else:
                    pan_angle -= PAN_STEP

            if abs(error_y) > Y_TOLERANCE:
                if error_y > 0:
                    tilt_angle += TILT_STEP
                else:
                    tilt_angle -= TILT_STEP

            pan_angle = max(0, min(180, pan_angle))
            tilt_angle = max(0, min(180, tilt_angle))

            kit.servo[PAN_CHANNEL].angle = pan_angle
            kit.servo[TILT_CHANNEL].angle = tilt_angle

            # cv2.putText(frame, f"Pan:{pan_angle} Tilt:{tilt_angle}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            # cv2.putText(frame, f"ErrorX:{error_x} ErrorY:{error_y}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)

        cv2.imshow("Face Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Exiting...")

finally:
    cam.release()
    cv2.destroyAllWindows()
