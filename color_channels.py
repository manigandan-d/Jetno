import cv2
import numpy as np

dispW = 640
dispH = 480
flip = 2

gst_pipeline = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! \
          nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! \
          videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

if not cam.isOpened():
    raise Exception("Camera not detected!")

blank = np.zeros([dispH, dispW, 1], np.uint8)

while True:
    ret, frame = cam.read()

    if not ret:
        print("Camera not detected")
        break

    b, g, r = cv2.split(frame)

    blue = cv2.merge([b, blank, blank])
    green = cv2.merge([blank, g, blank])
    red = cv2.merge([blank, blank, r])

    merged = cv2.merge([b, g, r])

    cv2.imshow("Original", frame)

    cv2.imshow("Blue Channel", blue)
    cv2.imshow("Green Channel", green)
    cv2.imshow("Red Channel", red)

    cv2.imshow("Merged", merged)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
