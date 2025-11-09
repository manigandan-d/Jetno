import cv2
import numpy as np
from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

PAN_CHANNEL = 0
TILT_CHANNEL = 1

kit.servo[PAN_CHANNEL].actuation_range = 180 
kit.servo[TILT_CHANNEL].actuation_range = 180 
kit.servo[PAN_CHANNEL].set_pulse_width_range(500, 2500)
kit.servo[TILT_CHANNEL].set_pulse_width_range(500, 2500)

pan_angle = 90
tilt_angle = 90

kit.servo[PAN_CHANNEL].angle = pan_angle
kit.servo[TILT_CHANNEL].angle = tilt_angle

dispW = 640
dispH = 480
flip = 2

gst_pipeline = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! \
          nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! \
          videoconvert ! video/x-raw, format=BGR ! appsink'

def nothing(x):
    pass 

cam = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

center_x = dispW // 2
center_y = dispH // 2 

cv2.namedWindow("Trackbars")

cv2.createTrackbar("LH", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("UH", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("LS", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("US", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("LV", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("UV", "Trackbars", 255, 255, nothing)

print("Starting...")

try:
    while True:
        ret, frame = cam.read()

        if not ret:
            print("Camera not detected")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lh = cv2.getTrackbarPos("LH", "Trackbars")
        uh = cv2.getTrackbarPos("UH", "Trackbars")
        ls = cv2.getTrackbarPos("LS", "Trackbars")
        us = cv2.getTrackbarPos("US", "Trackbars")
        lv = cv2.getTrackbarPos("LV", "Trackbars")
        uv = cv2.getTrackbarPos("UV", "Trackbars")

        lower = np.array([lh, ls, lv])
        upper = np.array([uh, us, uv])

        mask = cv2.inRange(hsv, lower, upper)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)

            if area > 800:
                x, y, w, h = cv2.boundingRect(contour)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # cv2.drawContours(frame, [contour], -1, (255, 0, 0), 2)

                obj_cx = x + w//2 
                obj_cy = y + h//2 
                cv2.circle(frame, (obj_cx, obj_cy), 5, (0, 0, 255), -1)

                error_x = center_x - obj_cx
                error_y = center_y - obj_cy

                step_x = 1 if abs(error_x) > 15 else 0 
                step_y = 1 if abs(error_y) > 15 else 0 

                if error_x > 0:
                    pan_angle += step_x
                elif error_x < 0:
                    pan_angle -= step_x

                if error_y > 0:
                    tilt_angle += step_y
                elif error_y < 0:
                    tilt_angle -= step_y

                pan_angle = max(0, min(180, pan_angle))
                tilt_angle = max(0, min(180, tilt_angle))

                kit.servo[PAN_CHANNEL].angle = pan_angle
                kit.servo[TILT_CHANNEL].angle = tilt_angle

        cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)
        cv2.imshow("Object Tracking", frame)
        cv2.imshow("Mask", mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Exiting...")

finally:
    cam.release()
    cv2.destroyAllWindows()
