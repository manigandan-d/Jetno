import cv2
import numpy as np

points = [] 

def mouse_event(event, x, y, flags, param):
    global points, frame

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))

    elif event == cv2.EVENT_RBUTTONDOWN:
        b, g, r = frame[y, x]  
        color_img = np.zeros((200, 200, 3), dtype=np.uint8)
        color_img[:] = [b, g, r]  
        cv2.putText(color_img, f"B:{b} G:{g} R:{r}", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.imshow("Color Picked", color_img)

dispW = 640
dispH = 480
flip = 2

gst_pipeline = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! \
          nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! \
          videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

cv2.namedWindow("Live")
cv2.setMouseCallback("Live", mouse_event)

while True:
    ret, frame = cam.read()
    if not ret:
        break

    for (x, y) in points:
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        cv2.putText(frame, f"{x},{y}", (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow("Live", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):  
        points = []
    elif key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
